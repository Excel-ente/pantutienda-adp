from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.urls import reverse
from django.utils.html import format_html

# Inline relacionado 
class DireccionEntregaClienteInline(admin.StackedInline):
    model = DireccionEntregaCliente
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('direccion','entre_calle_1','entre_calle_2','hora_desde','hora_hasta','comentarios','pin_maps')#'boton_maps',
    #readonly_fields = ('boton_maps',)

    class Media:
        js = ('admin/js/maps_popup.js',)  # Incluye el JavaScript personalizado

    def boton_maps(self, obj):
        """Botón que abre Google Maps en un popup."""
        return format_html(
            '<button type="button" class="btn btn-dark" onclick="openGoogleMapsPopup(\'id_pin_maps\', \'id_direccion\')">'
            '📍 Abrir 🗺️</button>'
        )

    boton_maps.short_description = "🗺️"

# Inline relacionado 
class OnboardingProveedorInline(admin.StackedInline):
    model = OnboardingProveedor  
    extra = 0  
    can_delete = False 
    fields = ('nombre_empresa', 'cuit', 'direccion', 'telefono_contacto', 'horario_atencion','aprobado','boton_maps','pin_maps')
    readonly_fields = ('aprobado','boton_maps',)

    class Media:
        js = ('admin/js/maps_popup.js',)  # Incluye el JavaScript personalizado

    def boton_maps(self, obj):
        """Botón que abre Google Maps en un popup."""
        return format_html(
            '<button type="button" class="btn btn-dark" onclick="openGoogleMapsPopup(\'id_pin_maps\', \'id_direccion\')">'
            '📍 Abrir 🗺️</button>'
        )

    boton_maps.short_description = "🗺️"
# -----------------------------------------------------------------------------
# Vista Vendedor
#    
@admin.register(Flota)
class FlotaAdmin(ImportExportModelAdmin):
    list_display = ('patente', 'vehiculo','habilitado')
    exclude = ('fecha_habilitacion',)

# -----------------------------------------------------------------------------
# Vista Vendedor
#    
@admin.register(Vendedor)
class VendedorAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'apellido','estado_cuenta','estado')
    exclude = ('habilitado',)
    readonly_fields = ('estado_cuenta','deshabilitar',)

    def estado_cuenta(self,obj):
        return f'{obj.estado_cuenta()}'

    def deshabilitar(self,obj):
        if obj.habilitado:
            return format_html('<a class="btn btn-danger" style="border-radius:5px" href="{}">Deshabilitar</a>', reverse('deshabilitar-vendedor', args=[obj.id]))
        else:
            return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Habilitar</a>', reverse('habilitar-vendedor', args=[obj.id]))

    def estado(self, obj):
        if obj.habilitado:
            return f'🟢 Habilitado'
        else:
            return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Habilitar</a>', reverse('habilitar-vendedor', args=[obj.id]))


    # def has_add_permission(self, request, obj=None):
    #     # Disables the ability to add new records directly in the admin
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     # Disables the ability to change existing records directly in the admin
    #     return False

    def has_delete_permission(self, request, obj=None):
        # Disables the ability to delete existing records directly in the admin
        return False


# -----------------------------------------------------------------------------
# Vista Chofer
# 
@admin.register(Chofer)
class ChoferAdmin(ImportExportModelAdmin):
    list_display = ('usuario','estado_cuenta','estado')
    exclude = ('habilitado',)
    readonly_fields = ('estado_cuenta','deshabilitar',)

    def estado_cuenta(self,obj):
        return f'{obj.estado_cuenta()}'

    def deshabilitar(self,obj):
        if obj.habilitado:
            return format_html('<a class="btn btn-danger" style="border-radius:5px" href="{}">Deshabilitar</a>', reverse('deshabilitar-chofer', args=[obj.id]))
        else:
            return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Habilitar</a>', reverse('habilitar-chofer', args=[obj.id]))

    def estado(self, obj):
        if obj.habilitado:
            return f'🟢 Habilitado'
        else:
            return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Habilitar</a>', reverse('habilitar-chofer', args=[obj.id]))


    def has_delete_permission(self, request, obj=None):
        # Disables the ability to delete existing records directly in the admin
        return False
# -----------------------------------------------------------------------------
# Vista proveedor
# 
@admin.register(Proveedor)
class ProveedorAdmin(ImportExportModelAdmin):
    list_display = ('id','usuario','emprendimiento','estado_cuenta','estado',)
    list_filter = ('habilitado',)
    readonly_fields = ('fecha_alta','fecha_habilitacion','habilitado','deshabilitar')
    search_fields = ('usuario','emprendimiento')

    inlines = [OnboardingProveedorInline]

    def emprendimiento(self,obj):
        emprendimiento = OnboardingProveedor.objects.filter(proveedor=obj).first()
        if emprendimiento:
            return emprendimiento.nombre_empresa
        else:
            return 'Sin Emprendimiento'

    def has_delete_permission(self, request, obj=None):
        # Disables the ability to delete existing records directly in the admin
        return False
    
    def estado_cuenta(self,obj):
        return f'{obj.estado_cuenta()}'
    
    def deshabilitar(self,obj):
        if obj.habilitado:
            return format_html('<a class="btn btn-danger" style="border-radius:5px" href="{}">Deshabilitar</a>', reverse('deshabilitar-proveedor', args=[obj.id]))
        else:
            return f'-'

    def estado(self, obj):
        if obj.habilitado:
            return f'🟢 Habilitado'
        else:
            emprendimiento = OnboardingProveedor.objects.filter(proveedor=obj).first()
            if emprendimiento and not emprendimiento.aprobado:
                return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Habilitar</a>', reverse('habilitar-proveedor', args=[obj.id]))
            else:
                return f'-'

    def changelist_view(self, request, extra_context=None):

        cards = True

        # Calculamos los datos para las tarjetas
        total_proveedores = Proveedor.objects.count()
        proveedores_habilitados = Proveedor.objects.filter(habilitado=True).count()
        proveedores_deshabilitados = Proveedor.objects.filter(habilitado=False).count()
        proveedores_recientes = Proveedor.objects.filter(fecha_alta__gte="2023-01-01").count()

        etiqueta_1 = 'Total Proveedores'
        val_etiqueta_1 = total_proveedores
        etiqueta_2 = 'Proveedores Habilitados'
        val_etiqueta_2 = proveedores_habilitados
        etiqueta_3 = 'Proveedores Deshabilitados'
        val_etiqueta_3 = proveedores_deshabilitados
        etiqueta_4 = 'Proveedores Recientes'
        val_etiqueta_4 = proveedores_recientes

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
        
        return super(ProveedorAdmin, self).changelist_view(request, extra_context=extra_context)
                                                           
# -----------------------------------------------------------------------------
# Vista Cliente
# 
@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    list_display = ('id','usuario','cuenta_corriente','estado')
    readonly_fields = ('estado','fecha_alta','deshabilitar')
    exclude = ('habilitado','fecha_alta','fecha_habilitacion')
    list_display_links = ('id','usuario',)
    search_fields = ('usuario','codigo')
    list_filter = ('id','codigo','tipo_cliente','usuario')
    inlines = [DireccionEntregaClienteInline,]

    def has_delete_permission(self, request, obj=None):
        # Disables the ability to delete existing records directly in the admin
        return False
    
    def cuenta_corriente(self, obj):
        if obj.habilitar_cc:
            total_deuda = 0
            cuenta_corriente = total_deuda
            if cuenta_corriente > 0:
                return f'🔴 Debe $ {" {:,.2f}".format(cuenta_corriente)}'
            elif cuenta_corriente == 0:
                return f'🟢 Al dia'
            else:
                return f'🔵 A favor $ {" {:,.2f}".format(cuenta_corriente)}'
        else:
            return '😔 No Habilitada'
            
    def changelist_view(self, request, extra_context=None):

        cards = True
        moneda = '$'

        # Calculamos los datos para las tarjetas
        total_clientes = Cliente.objects.count()
        clientes_habilitados = Cliente.objects.filter(habilitado=True).count()
        cuenta_corriente = 0
        cobrado_a_clientes = 0

        etiqueta_1 = 'Total Clientes'
        val_etiqueta_1 = total_clientes
        etiqueta_2 = 'Clientes Habilitados'
        val_etiqueta_2 = clientes_habilitados
        etiqueta_3 = 'Cuenta Corriente'
        val_etiqueta_3 = f'{moneda} {cuenta_corriente:,.2f}'
        etiqueta_4 = 'Cobros'
        val_etiqueta_4 = f'{moneda} {cobrado_a_clientes:,.2f}'

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
        
        return super(ClienteAdmin, self).changelist_view(request, extra_context=extra_context)
    
    def deshabilitar(self,obj):
        if obj.habilitado:
            return format_html('<a class="btn btn-danger" style="border-radius:5px" href="{}">Deshabilitar</a>', reverse('deshabilitar-cliente', args=[obj.id]))
        else:
            return f'-'

    def estado(self, obj):
        if obj.habilitado:
            return f'🟢 Habilitado'
        else:
            direccion = DireccionEntregaCliente.objects.filter(Cliente=obj).first()
            if direccion:
                return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Habilitar</a>', reverse('habilitar-cliente', args=[obj.id]))
            else:
                return f'Sin Direccion de Entrega'










