from django.contrib import admin
from django.db.models import Sum,Count
from configuracion.models import configuracion
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin
from django.db.models import Sum, F, Value, Case, When, DecimalField, IntegerField
from django.http import HttpResponseRedirect

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

# class NotaCreditoEnCompraInline(admin.TabularInline):
    # show_change_link = True
    # model = NotaDeCreditoCompra
    # extra = 0
    # readonly_fields = ('fecha','compra','motivo','estado')

    # def has_view_permission(self, request, obj=None):
    #     return True


    # def has_add_permission(self, request, obj=None):
    #     return False 
    
    # def has_delete_permission(self, request, obj=None):
    #     return False 

# class detalleNotaCreditoInline(admin.StackedInline):

    # model = detalleNotaCredito
    # extra = 0
    # readonly_fields = ( 'Subtotal',)
    # fields = ('producto', 'Cantidad', 'Precio', 'Subtotal')

    # # def get_readonly_fields(self, request, obj=None):
    # #     if obj:
    # #         return self.readonly_fields + ('producto', 'Cantidad', 'Precio', 'Subtotal')
    # #     return self.readonly_fields

    # def Subtotal(self,obj):
    #     config = configuracion.objects.first()
    #     moneda = config.Moneda
    #     return f'{moneda} {obj.Subtotal():,.2f}'

class articulosCompraInline(admin.StackedInline):
    model = detalleCompra
    extra = 1
    list_per_page = 15
    fields = ('producto', 'cantidad', 'precio', 'descuento', 'Total_unitario', 'Total', 'ActualizarCosto', 'Presentacion','detalle')
    readonly_fields = ('Total_unitario', 'Total', 'Presentacion','detalle')

    # Sobrescribe el método get_fields para modificar dinámicamente los campos
    def get_fields(self, request, obj=None):
        # Verifica la configuración
        config = configuracion.objects.first()
        fields = ['producto', 'cantidad', 'precio', 'descuento', 'Total_unitario', 'Total', 'ActualizarCosto', 'Presentacion','detalle']
        
        if config and not config.confirmar_pisar_costo:
            # Ocultamos 'ActualizarCosto' si confirmar_pisar_costo es False
            fields.remove('ActualizarCosto')
        
        return fields
    
    def has_change_permission(self, request, obj=None):
        """Deshabilita la edición si la compra está confirmada."""
        if obj and obj.estado:  # Si la compra está confirmada
            return False
        return super().has_change_permission(request, obj)
    
    def Presentacion(self,obj):
        texto=obj.presentacion()
        return texto

    def Total_unitario(self, obj):
        config = configuracion.objects.first()
        return f'{config.Moneda.signo} {obj.precio_calculado:,.2f}'

    def Total(self, obj):
        config = configuracion.objects.first()
        return f'{config.Moneda.signo} {obj.total_calculado:,.2f}'

class FleteCompraInline(admin.StackedInline):
    model = FleteCompra
    extra = 0
    fields = (
        'importe',
        'chofer',
        'vehiculo',
        'direccion_retiro',
        'direccion_descarga',
        'comentarios',
        )

    exclude=('cancelado',)

    def has_change_permission(self, request, obj=None):
        """Deshabilita la edición si la compra está confirmada."""
        if obj and obj.estado:  # Si la compra está confirmada
            return False
        return super().has_change_permission(request, obj)


class CompraResource(resources.ModelResource):
    # Definimos los campos a exportar e importar
    id = fields.Field(attribute='id', column_name='ID')
    fecha = fields.Field(attribute='fecha', column_name='Fecha')
    proveedor = fields.Field(
        column_name='Proveedor',
        attribute='proveedor',
        widget=ForeignKeyWidget(Proveedor, 'nombre')  # Accedemos al nombre del proveedor
    )
    total = fields.Field(attribute='total', column_name='Total')
    estado = fields.Field(attribute='estado', column_name='Estado')
    en_transito = fields.Field(attribute='en_transito', column_name='En Transito')

    class Meta:
        model = Compra  # Modelo al que corresponde este resource
        fields = ('id', 'fecha', 'proveedor', 'total', 'estado', 'en_transito')  # Campos a incluir
        export_order = ('id', 'fecha', 'proveedor', 'total', 'estado', 'en_transito')  # Orden de exportación

    def dehydrate_estado(self, compra):
        """Transforma el campo 'estado' a texto."""
        return 'Confirmada' if compra.estado else 'Pendiente'

    def dehydrate_en_transito(self, compra):
        """Transforma el campo 'en_transito' a texto."""
        return 'Sí' if compra.en_transito else 'No'
    

@admin.register(Compra)
class CompraAdmin(ImportExportModelAdmin):
    resource_class = CompraResource
    list_display = ('id','Proveedor','IMPORTE','ACCIONES',)#'ver_maps'
    list_display_links = ('id','Proveedor',)
    list_filter = ('id','proveedor','en_transito','en_descarga','en_transito','anulada')
    readonly_fields = ('detalle',)
    show_full_result_count = False
    exclude = ('total', 'en_transito','descargas','compra_inicial','estado','anulada','anulada_el','anulada_por','en_descarga',)
    date_hierarchy = 'fecha'
    list_per_page = 15
    inlines = [articulosCompraInline,FleteCompraInline,]

    def ACCIONES(self, obj):
        config = configuracion.objects.first()
        valor = float(obj.total_compra())
        articulos = detalleCompra.objects.filter(compra=obj).count()

        if not obj.estado:  # Si la compra no está confirmada
            if articulos == 0:
                return "📦 Ingrese artículos"
            if valor <= 0:
                return "⚠️ El valor total no puede ser 0"
            
            # Botón de Confirmar Compra
            return format_html(
                '''
                <a class="btn btn-dark" href="#" onclick="showCustomConfirm('{}')">Confirmar 🆗</a>
                <div id="custom-confirm" class="modal">
                    <div class="modal-content">
                        <span class="close">&times;</span>
                        <h4>¿Confirmar esta compra?</h4>
                        <p>Una vez confirmada, no podrá modificarse.</p>
                        <button id="confirm-btn" class="btn-custom-ok">Confirmar</button>
                        <button id="cancel-btn" class="btn-custom-cancel">Cancelar</button>
                    </div>
                </div>
                ''',
                reverse('confirmar_compra', args=[obj.id])
            )

        elif obj.en_transito:  # Si la compra está en tránsito
            return format_html(
                '<a class="btn btn-dark" href="{}">Llegada 🚚</a>',
                reverse('iniciar_descarga', args=[obj.id])
            )

        elif obj.en_descarga:  # Si está en proceso de descarga
            return format_html(
                '<a class="btn btn-dark" href="{}">Finalizar Descarga ✅</a>',
                reverse('terminar_descarga', args=[obj.id])
            )

        return "🟢 Proceso finalizado"
    ACCIONES.short_description = "ESTADO"

    def get_readonly_fields(self, request, obj=None):
        """Controla los campos de solo lectura dinámicamente."""
        config = configuracion.objects.first()

        # Por defecto, estos campos serán de solo lectura
        readonly_fields = ['id','Proveedor','estado', 'detalle']

        # Si 'editar_fecha_compra' es False, agrega 'fecha' como readonly
        if not config.editar_fecha_compra:
            readonly_fields.append('fecha')

        return readonly_fields
    
    def get_fields(self, request, obj=None):
        """
        Controla los campos que se muestran en el formulario.
        Si la compra está confirmada, solo muestra ciertos campos en modo lectura.
        """
        if obj and obj.estado:  # Si la compra está confirmada
            #return [field.name for field in self.model._meta.fields]
            return ['id', 'Proveedor','estado','detalle']
        return super().get_fields(request, obj)
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Incluye el CSS personalizado
        }
        js = ('admin/js/custom_admin.js',)  # Incluye el JS personalizado

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('proveedor', 'deposito')  

    def changelist_view(self, request, extra_context=None):
        # Obtener el queryset filtrado del ChangeList
        response = super().changelist_view(request, extra_context=extra_context)

        # Si la respuesta es una redirección, no intentamos acceder a context_data
        if isinstance(response, HttpResponseRedirect):
            return response

        try:
            # Obtener el queryset y aplicar optimización diferida
            cl = response.context_data['cl']
            queryset = cl.queryset.defer('observacion')
        except (KeyError, AttributeError):
            queryset = self.get_queryset(request).defer('observacion')

        # Usar aggregate con output_field para evitar errores de tipo
        totals = queryset.aggregate(
            total_compras=Count('id', output_field=IntegerField()),  # Contador de compras
            total_compras_monto=Sum('total', output_field=DecimalField()),  # Suma del total
            total_pendientes=Sum(
                Case(When(estado=False, then=1), default=0, output_field=IntegerField())
            ),
            total_pendientes_monto=Sum(
                Case(When(estado=False, then=F('total')), default=0, output_field=DecimalField())
            ),
            total_en_transito=Sum(
                Case(When(en_transito=True, then=1), default=0, output_field=IntegerField())
            ),
            total_en_transito_monto=Sum(
                Case(When(en_transito=True, then=F('total')), default=0, output_field=DecimalField())
            ),
            total_en_descarga=Sum(
                Case(When(en_descarga=True, then=1), default=0, output_field=IntegerField())
            ),
            total_en_descarga_monto=Sum(
                Case(When(en_descarga=True, then=F('total')), default=0, output_field=DecimalField())
            )
        )

        # Añadir los resultados al contexto
        extra_context = extra_context or {}
        extra_context.update(
            {
            'cards_doble': True,
            
            'emoji_1':f'📦',
            'etiqueta_1': 'Total Compras',
            'label_val_etiqueta_1' : f'Total:',
            'val_etiqueta_1': f"{totals['total_compras'] or 0:,}",

            'label_sub_val_etiqueta_1' : f'Importe:',
            'sub_val_etiqueta_1': f"$ {totals['total_compras_monto'] or 0:,.2f}",

            'emoji_2': f'🛒',
            'etiqueta_2': 'Compras Pendientes',
            'label_val_etiqueta_2' : f'Total:',
            'val_etiqueta_2': f"{totals['total_pendientes'] or 0:,}",
            'label_sub_val_etiqueta_2' : f'Importe:',
            'sub_val_etiqueta_2': f"$ {totals['total_pendientes_monto'] or 0:,.2f}",

            'emoji_3': f'🚚',
            'etiqueta_3': 'Compras en Tránsito',
            'label_val_etiqueta_3' : f'Total:',
            'val_etiqueta_3': f"{totals['total_en_transito'] or 0:,}",
            'label_sub_val_etiqueta_3' : f'Importe:',
            'sub_val_etiqueta_3': f"$ {totals['total_en_transito_monto'] or 0:,.2f}",

            'emoji_4': f'📦',
            'etiqueta_4': 'Descargando',
            'label_val_etiqueta_4' : f'Total:',
            'val_etiqueta_4': f"{totals['total_en_descarga'] or 0:,}",
            'label_sub_val_etiqueta_4' : f'Importe:',
            'sub_val_etiqueta_4': f"$ {totals['total_en_descarga_monto'] or 0:,.2f}",


        }
        )

        # Actualizar el contexto y devolver la respuesta
        response.context_data.update(extra_context)
        return response

    def change_view(self, request, object_id, form_url='', extra_context=None):


        # Obtenemos la compra actual
        compra = self.get_object(request, object_id)

        # Cálculos para las tarjetas
        total_articulos = detalleCompra.objects.filter(compra=compra).aggregate(total=Sum('cantidad'))['total'] or 0
        total_sin_flete = sum(detalle.total for detalle in detalleCompra.objects.filter(compra=compra))
        total_flete = compra.total_flete()

        
        monto_total_compra = compra.total_compra()
        notas_credito = compra.nc_asociada()
        estado_compra = '🟢 Confirmada' if compra.estado else '🟠 Pendiente'

        # Añadimos estos datos al contexto
        extra_context = extra_context or {}
        extra_context['cards_doble'] = True

        # Tarjeta 1: Total Productos
        extra_context['etiqueta_1'] = "Total Productos"
        extra_context['val_etiqueta_1'] = f"📦 {total_articulos:,.0f}"
        extra_context['sub_val_etiqueta_1'] = f"🛒 $ {total_sin_flete:,.2f}"

        # Tarjeta 2: Total Flete
        extra_context['etiqueta_2'] = "Total Flete"
        extra_context['val_etiqueta_2'] = f"🚚 {FleteCompra.objects.filter(compra=compra).count()} fletes"
        extra_context['sub_val_etiqueta_2'] = f"🛻 $ {total_flete:,.2f}"

        # Tarjeta 3: Monto Total Compra
        extra_context['etiqueta_3'] = "Monto Total de la Compra"
        extra_context['val_etiqueta_3'] = f"💰 $ {monto_total_compra:,.2f}"
        extra_context['sub_val_etiqueta_3'] = (
            f"📕 Nota de Crédito Aplicada" if notas_credito else "📗 Sin Notas de Crédito"
        )

        # Tarjeta 4: Estado de la Compra
        extra_context['etiqueta_4'] = "Estado de la Compra"
        extra_context['val_etiqueta_4'] = estado_compra
        extra_context['sub_val_etiqueta_4'] = (
            "🚚 En tránsito" if compra.en_transito else 
            "📦 En descarga" if compra.en_descarga else 
            "💵 En espera"
        )

        # Llamada a la vista original del formulario
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def Proveedor(self, obj):
        proveedor = obj.proveedor
        return proveedor if proveedor else "Proveedores Generales"

    def IMPORTE(self, obj):
        moneda = configuracion.objects.first().Moneda.signo
        importe = obj.total_compra()
        total = f'{moneda} {importe:,.2f}'
        url = reverse('popup_comparar_productos', args=[obj.id])
        return format_html('{} &nbsp;<a class="btn btn-dark" style="border-radius:15px;padding: 5px;" href="{}">📉</a>',total, url)
        
    def ver_maps(self, obj):
        flete = FleteCompra.objects.filter(compra=obj).first()
        if flete and flete.ruta_maps:
            return format_html('<a class="btn btn-info" target="_Blank" href="{}">🗺️</a>', reverse('ver_google_maps', args=[obj.id]))
        return ""
    ver_maps.short_description = 'MAPA'

@admin.register(detalleCompra)
class DetalleCompraAdmin(ImportExportModelAdmin):
    list_display_links = None
    list_display = ('compra_link','PRODUCTO','cantidad','precio_unitario',)#'subtotal'
    readonly_fields = ('compra','producto','cantidad','precio','descuento','subtotal','ActualizarCosto','detalle')
    list_filter = ('compra','producto',)
    date_hierarchy = 'fecha'
    list_per_page = 30
    exclude=('precio','deposito','total')

    def get_queryset(self, request):
        """Filtra para mostrar solo productos de compras con estado=True."""
        qs = super().get_queryset(request)
        return qs.filter(compra__estado=True)

    def compra_link(self, obj):
        # Usa reverse para generar el enlace a la página de detalles de la compra
        url = reverse('admin:compras_compra_change', args=[obj.compra.id])
        return format_html('<b>{}</b> &nbsp;<a class="btn btn-dark" style="border-radius:5px;padding: 5px;" href="{}">Ver</a>', obj.compra.pk, url)
    compra_link.short_description = 'Compra'

    def precio_unitario(self, obj):
        config = configuracion.objects.first()
        moneda = config.Moneda.signo
        precio = obj.precio
        return str(moneda) + str(" {:,.2f}".format(precio))
    
    def subtotal(self, obj):
        moneda = configuracion.objects.first()
        return str(moneda.Moneda.signo) + str(" {:,.2f}".format(obj.total))
    

    def PRODUCTO(self, obj):
        # Usa reverse para generar el enlace a la página de detalles de la compra
        url = reverse('admin:compras_detallecompra_change', args=[obj.id])
        return format_html('<b>{}</b> &nbsp;<a class="btn btn-dark" style="border-radius:5px;padding: 5px;" href="{}">Ver</a>', obj.producto.nombre, url)

















# @admin.register(NotaDeCreditoCompra)
# class NotaDeCreditoCompraAdmin(admin.ModelAdmin):
#     form = NotaDeCreditoCompraForm
#     list_display = ('fecha', 'compra', 'motivo', 'total', 'ACCIONES',)
#     exclude = ('anulada','anulada_el','anulada_por','entregado','estado')
#     inlines = [detalleNotaCreditoInline,]

#     def get_form(self, request, obj=None, **kwargs):
#         form = super(NotaDeCreditoCompraAdmin, self).get_form(request, obj, **kwargs)
#         return form

#     def save_model(self, request, obj, form, change):
#         obj.save()
#         if not change:  # Si es una nueva Nota de Crédito
#             for detalle in obj.compra.detallecompra_set.all():
#                 detalleNotaCredito.objects.create(
#                     NotaCredito=obj,
#                     producto=detalle.producto,
#                     Cantidad=detalle.Cantidad,
#                     Precio=detalle.Precio
#                 )
#         super().save_model(request, obj, form, change)

#     def ACCIONES(self, obj):
#         if obj.id is not None:  # Verifica si el ID no es None

#             if obj.estado == False:
#                 return format_html('<a class="btn btn-danger" href="{}">🆗</a>', reverse('autorizar_nc', args=[obj.id]))

#             if obj.entregado == False:
#                 return format_html('<a class="btn" style="background-color: rgba(54, 162, 235, 0.6);" href="{}">📦 Entregar articulos</a>', reverse('entregar_articulos_nc', args=[obj.id]))
#             else:
#                 return f'✅ Confirmada.'
       
#         return '❌ Sin ID'

#     def total(self, obj):
#         config = configuracion.objects.first()
#         moneda = config.Moneda
#         return str(moneda.Abreviacion) + str(" {:,.2f}".format(obj.total_nc()))



