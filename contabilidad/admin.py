from .models import *
from import_export.admin import ImportExportModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin


# Inline for MovimientosCuenta associated with CuentasComerciales
class MovimientosCuentaComercialinline(admin.TabularInline):
    model = MovimientosCuentaComercial
    extra = 0
    can_delete = False
    readonly_fields = ('comentarios', 'Debe', 'Haber')
    exclude = ('tipo', 'debe', 'haber',)

    def Debe(self, obj):
        # Format debe (debit) field for display
        return "{:,.2f}".format(obj.debe)

    def Haber(self, obj):
        # Format haber (credit) field for display
        return "{:,.2f}".format(obj.haber)

    def has_add_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return False

    def has_change_permission(self, request, obj=None):
        # Disables the ability to change existing records directly in the admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Disables the ability to delete existing records directly in the admin
        return False


# Inline for MovimientosCuenta associated with CuentasContables
class MovimientosCuentaContableinline(admin.TabularInline):
    model = MovimientosCuentaContable
    extra = 0
    can_delete = False
    readonly_fields = ('tipo_movimiento', 'Debe', 'Haber')
    exclude = ('fecha', 'tipo', 'cuenta_comercial', 'comentarios', 'debe', 'haber')

    def Debe(self, obj):
        # Format debe (debit) field for display
        return "{:,.2f}".format(obj.debe)

    def Haber(self, obj):
        # Format haber (credit) field for display
        return "{:,.2f}".format(obj.haber)

    def tipo_movimiento(self, obj):
        # Displays the related account or commercial account
        if obj.cuenta:
            return obj.cuenta
        return obj.cuenta_comercial
    tipo_movimiento.short_description = "Cuenta"

    def has_add_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return False

    def has_change_permission(self, request, obj=None):
        # Disables the ability to change existing records directly in the admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Allows the ability to delete records in the admin
        return True


# Admin for Cuentas model
@admin.register(Cuentas)
class CuentasContablesAdmin(ImportExportModelAdmin):
    # Fields to display in the list view
    list_display = ('tipo_cuenta', 'numero', 'descripcion', 'saldo')
    # Fields that will be read-only
   # readonly_fields = ('tipo_cuenta', 'numero', 'descripcion','moneda', )
    # Fields to filter the records by
    list_filter = ('numero', 'descripcion', 'tipo_cuenta')
    # Pagination size for the list view
    list_per_page = 25
    # Inline for MovimientosCuentaContableinline
    inlines = [MovimientosCuentaContableinline,]

    def saldo(self, obj):
        # Format the account balance for display
        return "{:,.2f}".format(obj.saldo_actual)

    def tipo_cuenta(self, obj):
        # Return the account type
        return obj.tipo_cuenta


# Admin for CuentasComerciales model
@admin.register(CuentasComerciales)
class CuentasComercialesAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'tipo', 'asociado', 'saldo')
    list_display_links = ('numero', 'asociado', 'tipo', 'saldo')
    readonly_fields = ('id','numero','moneda', 'asociado', 'tipo', 'saldo', 'vendedor','cliente','chofer','proveedor','descripcion')
    list_filter = ('numero',)
    list_per_page = 20
    inlines = [MovimientosCuentaComercialinline,]
    #search_fields = ('cliente__nombre', 'cliente__apellido', 'proveedor__Empresa', 'proveedor__NombreApellido')
    
    def has_delete_permission(self, request, obj=None):
        # Disables the ability to delete existing records directly in the admin
        return False
    
    def save_model(self, request, obj, form, change):
        # Custom save logic to assign numero if it's not set
        super().save_model(request, obj, form, change)
        if not obj.numero:
            try:
                obj.numero = obj.pk  # Assign the object's primary key to numero
                obj.save() 
            except:
                pass

    def tipo(self, obj):
        # Determines the type based on related fields (cliente, chofer, proveedor)
        if obj.cliente:
            return f'💸👤 Clientes'
        elif obj.vendedor:
            return f'👨🏻‍💼👩🏻‍💼 Vendedor'
        elif obj.chofer:
            return f'🚚👤 Choferes'
        elif obj.proveedor:
            return f'🪪👤 Proveedor'
        else:
            return '-'
        
    def asociado(self, obj):
        # Returns the associated person or company name
        if obj.cliente:
            return f'{obj.cliente.nombre_apellido}'
        elif obj.vendedor:
            return f'{obj.vendedor.nombre}'
        elif obj.chofer:
            return f'{obj.chofer.usuario.username}'
        elif obj.proveedor:
            return f'{obj.proveedor.usuario} ({obj.proveedor.empresa()})'
        else:
            return '-'

    def saldo(self, obj):
        saldo_actual = obj.saldo_actual
        return f'{saldo_actual:,.2f}'


    def changelist_view(self, request, extra_context=None):

        cards = True

        # Calculamos los datos para las tarjetas
        total_clientes = 0
        proveedores_vendedores = 0
        proveedores_choferes = 0
        proveedores_proveedores = 0

        etiqueta_1 = 'Resumen Clientes'
        val_etiqueta_1 = f'{total_clientes:,.2f}'
        etiqueta_2 = 'Resumen Vendedores'
        val_etiqueta_2 = f'{proveedores_vendedores:,.2f}'
        etiqueta_3 = 'Resumen Choferes'
        val_etiqueta_3 = f'{proveedores_choferes:,.2f}'
        etiqueta_4 = 'Resumen Proveedores'
        val_etiqueta_4 = f'{proveedores_proveedores:,.2f}'

        # Añadimos estos datos al contexto de la plantilla
        extra_context = extra_context or {'new_window': False,}
        
        extra_context['cards'] = cards
        extra_context['etiqueta_1'] = etiqueta_1
        extra_context['etiqueta_2'] = etiqueta_2
        extra_context['etiqueta_3'] = etiqueta_3
        extra_context['etiqueta_4'] = etiqueta_4
        extra_context['val_etiqueta_1'] = val_etiqueta_1
        extra_context['val_etiqueta_2'] = val_etiqueta_2
        extra_context['val_etiqueta_3'] = val_etiqueta_3
        extra_context['val_etiqueta_4'] = val_etiqueta_4
        
        return super(CuentasComercialesAdmin, self).changelist_view(request, extra_context=extra_context)
    
# Admin for Asientos model
@admin.register(Asientos)
class AsientosAdmin(ImportExportModelAdmin):
    # Fields to display in the list view
    list_display = ('id', 'fecha', 'detalle')
    # Fields to filter the records by
    list_filter = ('id', 'detalle')
    # Inline for MovimientosCuentaContableinline
    inlines = (MovimientosCuentaContableinline,)
    # Fields that will be read-only
    readonly_fields = ('fecha', 'detalle')
    # Pagination size for the list view
    list_per_page = 25

    # def get_queryset(self, request):
    #     # Custom queryset to exclude specific asientos
    #     qs = super().get_queryset(request)
    #     return qs.exclude(excluir_mov=True)

    def Status(self, obj):
        # Displays the status of the asiento
        if obj.estado:
            return '🟢 Registrado'
        return '🟠 Pendiente'

    def has_add_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return False

    def has_change_permission(self, request, obj=None):
        # Disables the ability to change existing records directly in the admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Allows the ability to delete records in the admin
        return True
