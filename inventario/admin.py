from django.contrib import admin
from django.db.models import F, Sum
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources, fields, widgets
from django.contrib import messages
from django.utils import timezone

# -----------------------------------------------------------------------------
# Vista Deposito
#

@admin.register(ProductoPrecio)
class ProductoPrecioAdmin(ImportExportModelAdmin):
    list_display =('id','lista','producto','presentacion','cantidad','unidad_de_medida','precio_unitario')
    readonly_fields =('id','lista','producto','presentacion','cantidad','unidad_de_medida','precio_unitario')


    def has_add_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return False

    def has_change_permission(self, request, obj=None):
        # Disables the ability to change existing records directly in the admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Disables the ability to delete existing records directly in the admin
        return True

# -----------------------------------------------------------------------------
# Vista Deposito
# 
@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display =('id','nombre',)


@admin.register(MovimientoProducto)
class MovimientoProductoAdmin(ImportExportModelAdmin):
    list_display = ('fecha','detalle','comentarios')
    exclude = ('estado',)
    readonly_fields = ('comentarios',)

    def comentarios(self,obj):
        if obj.estado:
            texto = f'🛻 En Tránsito'
        else:
            texto = f'🟢 Confirmado'
        return texto

    def has_add_permission(self, request, obj=None):
        return False  # Desactivar la capacidad de añadir nuevas ventas desde el admin de Cliente

    def has_change_permission(self, request, obj=None):
        return False  # Desactivar la capacidad de editar ventas desde el admin de Cliente

    def has_delete_permission(self, request, obj=None):
        return True  # Desactivar la capacidad de eliminar ventas desde el admin de Cliente



# -----------------------------------------------------------------------------
# Vista Deposito
# 
@admin.register(Deposito)
class DepositoAdmin(ImportExportModelAdmin):
    list_display = ('nombre','telefono')
    readonly_fields = ('boton_maps',)

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
# Vista Presentacion
# 
@admin.register(Presentacion)
class PresentacionAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)#
    list_per_page = 15

# -----------------------------------------------------------------------------
# Vista Producto
# 
# Vista para el precio d
class RecetaProductoInline(admin.StackedInline):
    model = RecetaProducto
    extra = 1
    fk_name = 'producto_principal'
    fields = ('producto_usado','cantidad','unidad_de_medida','Costo_calculado',)
    readonly_fields = ('Costo_calculado',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('producto_usado')

    def Costo_calculado(self, obj):
        moneda = configuracion.objects.first().Moneda
        return f"{moneda.signo} {obj.Costo_calculado():,.2f}"


# Vista para el precio del producto en el modelo de producto
class ProductoPrecioInline(admin.StackedInline):
    model = ProductoPrecio
    extra = 0
    readonly_fields = ('Costo_unitario', 'Precio_unitario','Rentabilidad')

    def get_fields(self, request, obj=None):
        """Determina los campos que se muestran en el inline, basados en la configuración."""
        fields = ['lista', 'presentacion', 'cantidad', 'unidad_de_medida', 'precio_manual', 'rentabilidad', 'Costo_unitario', 'Precio_unitario',]

        config = configuracion.objects.first()
        if config:
            if config.precio_venta_automatico:
                fields.remove('precio_manual')
            else:
                fields.remove('rentabilidad')

            if config.unidad_de_medida_precio_venta == False:
                fields.remove('unidad_de_medida')

        return fields


    def Rentabilidad(self, obj):
        return f"% {obj.rentabilidadNeta:,.2f}"

    def Costo_unitario(self, obj):
        moneda = configuracion.objects.first().Moneda
        return f"{moneda.signo} {obj.costo_unit():,.2f} x {obj.producto.unidad_de_medida}"

    def Precio_unitario(self, obj):
        moneda = configuracion.objects.first().Moneda
        return f"{moneda.signo} {obj.precio_unitario_calculado():,.2f} x 1 {obj.presentacion}"


# Vista para ver los movimientos del producto en el modelo de producto
class MovimientoProductoInline(admin.TabularInline):
    model = MovimientoProducto
    extra = 0
    can_delete = False
    fields = ('fecha','inventario','entrada','salida',)#'asiento',
    readonly_fields = ('fecha','inventario','entrada','salida',)#'asiento',

    def has_add_permission(self, request, obj=None):
        return False  # Desactivar la capacidad de añadir nuevas ventas desde el admin de Cliente

    def has_change_permission(self, request, obj=None):
        return False  # Desactivar la capacidad de editar ventas desde el admin de Cliente

    def has_delete_permission(self, request, obj=None):
        return False  # Desactivar la capacidad de eliminar ventas desde el admin de Cliente

# Vista Producto
# class ProductoResource(resources.ModelResource):
#     categoria = fields.Field(attribute='categoria__nombre', column_name='categoria', widget=widgets.ForeignKeyWidget(Categoria, 'nombre'))
#     primer_producto_precio = fields.Field(attribute='primer_producto_precio', column_name='primer_producto_precio')
#     stock_str = fields.Field(attribute='stock_str', column_name='stock_str')
#     valuacion_stock = fields.Field(attribute='valuacion_stock', column_name='valuacion_stock')
#     stock_str = fields.Field(attribute='stock_str', column_name='stock_str')

#     class Meta:
#         model = Producto
 
#     def dehydrate_primer_producto_precio(self, producto):
#         return producto.primer_producto_precio.precio_total if producto.primer_producto_precio else "No Disponible"

#     def dehydrate_stock_str(self, producto):
#         return producto.stock_actual_str

#     def dehydrate_valuacion_stock(self, producto):
#         return f'{producto.valuacion_stock:,.2f}'


def habilitar_productos_masivamente(modeladmin, request, queryset):
    # Iterar sobre los productos seleccionados
    for producto in queryset:
        if not producto.habilitar_venta:
            # Verificar si el producto puede ser habilitado (es publicable)
            if producto.es_publicable():
                producto.habilitar_venta = True
                producto.fecha_habilitacion = timezone.now()
                producto.save()
            else:
                messages.warning(request, f'El producto "{producto.nombre}" no puede ser publicado. Debe contener al menos 1 precio de venta.')
    # Mensaje de éxito general
    messages.success(request, f'Se habilitaron correctamente los productos seleccionados.')
habilitar_productos_masivamente.short_description = 'Habilitar productos seleccionados'

def deshabilitar_productos_masivamente(modeladmin, request, queryset):
    # Iterar sobre los productos seleccionados
    for producto in queryset:
        if producto.habilitar_venta:
            producto.habilitar_venta = False
            producto.save()
    messages.success(request, f'Se Deshabilitar correctamente los productos seleccionados.')
deshabilitar_productos_masivamente.short_description = 'Deshabilitar productos seleccionados'

from django.contrib.admin import SimpleListFilter

class StockFilter(SimpleListFilter):
    title = 'Stock'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return [
            ('con_stock', 'Con Stock'),
            ('sin_stock', 'Sin Stock'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'con_stock':
            # Filtramos productos con stock superior a 0
            return queryset.filter(
                id__in=[
                    producto.id for producto in queryset if producto.stock_actual > 0
                ]
            )
        elif self.value() == 'sin_stock':
            # Filtramos productos con stock igual o inferior a 0
            return queryset.filter(
                id__in=[
                    producto.id for producto in queryset if producto.stock_actual <= 0
                ]
            )
        return queryset


@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    #resource_class = ProductoResource
    list_display = ('mostrar_imagen','codigo','nombre','costo_ultimo_unitario','precio','en_inventario','publicado')
    list_display_links = ('mostrar_imagen','codigo','nombre','costo_ultimo_unitario','precio','en_inventario')
    readonly_fields = ['mostrar_imagen_form','proveedor','costo_ultimo_unitario','precio','stock_actual','deshabilitar',]
    list_filter = ('categoria','proveedor','habilitar_venta',StockFilter)
    list_per_page = 15
    search_fields = ('codigo','nombre')
    exclude = ('cantidad','proveedor''ultima_modificacion','habilitar_venta')#'costo_unitario','imagen',
    actions = [habilitar_productos_masivamente,deshabilitar_productos_masivamente]
    inlines = [ProductoPrecioInline,MovimientoProductoInline,RecetaProductoInline]

    # Solo muestra el inline si el producto es "compuesto"
    def get_inlines(self, request, obj=None):
        if obj and obj.tipo == 'Compuesto':
            return [ProductoPrecioInline,MovimientoProductoInline,RecetaProductoInline]
        else:
            return [ProductoPrecioInline,MovimientoProductoInline]
   
    def mostrar_imagen_form(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="200" height="200" style="border-radius:5px;"/>', obj.imagen.url)
        return "Sin imagen"
    mostrar_imagen_form.short_description = 'Imagen actual'

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;"/>', obj.imagen.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Imagen"
    
    def deshabilitar(self, obj):
        if obj.id is None:
            return "Producto no guardado"

        if obj.habilitar_venta:
            url = reverse('pausar-producto', args=[obj.id])
            return format_html('<a class="btn btn-danger" style="border-radius:5px" href="{}">Pausar</a>', url)
        else:
            url = reverse('habilitar-producto', args=[obj.id])
            return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Publicar</a>', url)

    def publicado(self, obj):
        if obj.id is None:
            return "Producto no guardado"

        if obj.habilitar_venta:
            return '🟢 Publicado'
        else:
            url = reverse('habilitar-producto', args=[obj.id])
            return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Publicar</a>', url)
        
     # Sobrescribe el método get_list_display para modificar dinámicamente las columnas
    
    def get_list_display(self, request):
        # Verifica la configuración
        config = configuracion.objects.first()
        if config and config.valuar_stock_negativo:
            # Si la configuración valuar_stock_negativo es True, mostramos 'codigo'
            return ('mostrar_imagen','codigo', 'nombre', 'costo_ultimo_unitario', 'precio', 'en_inventario', 'publicado')
        else:
            # Si no, ocultamos 'codigo'
            return ('mostrar_imagen','nombre', 'costo_ultimo_unitario', 'precio', 'en_inventario', 'publicado')
        
    def get_readonly_fields(self, request, obj=None):
        # Si el producto es de tipo compuesto, ocultar `costo_ultimo_unitario`
        fields = ['mostrar_imagen_form', 'proveedor', 'precio', 'stock_actual', 'deshabilitar']
        if obj and obj.tipo == 'Compuesto':
            fields.append('costo_unitario')
        return fields

    def en_inventario(self,obj):
        texto=obj.stock_actual_str
        return texto

    def costo_ultimo_unitario(self,obj):
        moneda = configuracion.objects.first().Moneda.signo
        if obj.tipo == 'Compuesto':
            precio_select = obj.costo_unitario_calculado()
        else:
            precio_select = obj.costo_unitario

        return f'{moneda} {precio_select:,.2f}'
    
    def precio(self,obj):
        moneda=configuracion.objects.first().Moneda.signo
        precio_select=obj.primer_producto_precio
        if precio_select:
            precio=precio_select.precio_unitario_calculado()
        else:
            precio=0
        return f'{moneda} {precio:,.2f}'

    def changelist_view(self, request, extra_context=None):

    
        moneda=configuracion.objects.first().Moneda.signo
        stock_negativo=configuracion.objects.first().valuar_stock_negativo

        # Calculamos los datos para las tarjetas
        total_productos = Producto.objects.count()
        productos_habilitados = Producto.objects.filter(habilitar_venta=True).count()

        # Calculamos la sumatoria de la valuación total recorriendo los productos
        productos = Producto.objects.all()
        valuacion_productos = sum([producto.valuacion_stock for producto in productos])

        inventario_negativo = sum([producto.valuacion_stock_negativo for producto in productos])

        etiqueta_1 = 'Total Productos'
        val_etiqueta_1 = f'📦 {total_productos:,.0f}'
        etiqueta_2 = 'Productos Habilitados'
        val_etiqueta_2 = f'🏁 {productos_habilitados:,.0f}'
        etiqueta_3 = 'Valuacion Productos'
        val_etiqueta_3 = f"{moneda} {valuacion_productos:,.2f}"
        etiqueta_4 = 'Inventario Negativo'
        val_etiqueta_4 = f"- {moneda} {-inventario_negativo:,.2f}"

        # Añadimos estos datos al contexto de la plantilla
        extra_context = extra_context or {'new_window': False,}
        
        extra_context['cards_simple'] = True
        extra_context['etiqueta_1'] = etiqueta_1
        extra_context['etiqueta_2'] = etiqueta_2
        extra_context['etiqueta_3'] = etiqueta_3
        extra_context['etiqueta_4'] = etiqueta_4
        extra_context['val_etiqueta_1'] = val_etiqueta_1
        extra_context['val_etiqueta_2'] = val_etiqueta_2
        extra_context['val_etiqueta_3'] = val_etiqueta_3
        extra_context['val_etiqueta_4'] = val_etiqueta_4
        
        return super(ProductoAdmin, self).changelist_view(request, extra_context=extra_context)


# -----------------------------------------------------------------------------
# Vista Producto
# 
