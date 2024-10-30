from django.contrib import admin

from .reporte_pedido import exportar_a_excel, exportar_a_pdf
from .models import Pedido, ItemPedido
from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

class ItemPedidoInline(admin.StackedInline):
    model = ItemPedido
    extra = 1  # Muestra un ítem vacío adicional por defecto
    fields = ('producto_precio','cantidad','Cantidad_solicitada','Precio_Unitario','Subtotal','disponibilidad')
    readonly_fields =('Cantidad_solicitada','Precio_Unitario','Subtotal','disponibilidad')

    def disponibilidad(self,obj):
        return f'{obj.consutlar_stock()}'

    def Cantidad_solicitada(self,obj):
        return  f'{obj.cantidad_madre():,.2f} {obj.producto.unidad_de_medida}'

    def Precio_Unitario(self,obj):
        return  f'{obj.precio_unitario:,.2f}'

    def Subtotal(self,obj):
        return f'{obj.subtotal():,.2f}'

    def has_delete_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return False

    def has_add_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display_links = ('numero_pedido', 'direccion_entrega_cliente',)
    list_display = ('numero_pedido', 'direccion_entrega_cliente','importe', 'estado','ACCIONES')
    list_filter = ('id','cliente', 'estado')  # Filtros por cliente y estado
    search_fields = ('cliente__usuario__username',)  # Búsqueda por nombre de usuario del cliente
    readonly_fields =('numero_pedido','cliente','direccion_entrega_cliente','estado')
    date_hierarchy = 'creado_en'  # Jerarquía por fecha
    exclude = ('cliente',)
    list_per_page = 20  # Paginación
    inlines = [ItemPedidoInline]
    actions = [exportar_a_excel, exportar_a_pdf]

    def numero_pedido(self,obj):
        return f'{obj.pk}'
    
    def importe(self, obj):
        """Devuelve el importe total del pedido"""
        return f'{obj.total():,.2f}'

    def get_queryset(self, request):
        # Sobrescribimos el queryset para excluir los pedidos con estado "Pendiente"
        qs = super().get_queryset(request)
        # Asumimos que el estado "Pendiente" es representado con un valor, por ejemplo, "pendiente"
        return qs.exclude(estado='abierto')
        
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        # Verificar que la respuesta no sea HttpResponseRedirect
        if hasattr(response, 'context_data'):
            try:
                # Obtener el ChangeList, que es responsable de aplicar los filtros y búsquedas
                cl = response.context_data['cl']
                queryset = cl.queryset
            except (KeyError, AttributeError):
                # Si hay un error al obtener el ChangeList, usar el queryset sin filtrar
                queryset = self.get_queryset(request)
            
            # Calcular las métricas
            total_pedidos = queryset.exclude(estado='abierto').count()
            pedidos_pendientes = queryset.filter(estado='pendiente').count()
            pedidos_procesando = queryset.filter(estado='en_preparacion').count()
            pedidos_listo = queryset.filter(estado='listo').count()
            pedidos_en_camino = queryset.filter(estado='en_camino').count()
            pedidos_completados = queryset.filter(estado='completado').count()
            pedidos_cancelados = queryset.filter(estado='cancelado').count()

            # Calcular ingresos totales por estado
            total_importe = queryset.exclude(estado='abierto').aggregate(
                total=Sum(F('items__precio_unitario') * F('items__cantidad'))
            )['total'] or 0
            importe_pendientes = queryset.filter(estado='pendiente').aggregate(
                total=Sum(F('items__precio_unitario') * F('items__cantidad'))
            )['total'] or 0
            importe_en_preparacion = queryset.filter(estado='en_preparacion').aggregate(
                total=Sum(F('items__precio_unitario') * F('items__cantidad'))
            )['total'] or 0
            importe_listo = queryset.filter(estado='listo').aggregate(
                total=Sum(F('items__precio_unitario') * F('items__cantidad'))
            )['total'] or 0
            importe_en_camino = queryset.filter(estado='en_camino').aggregate(
                total=Sum(F('items__precio_unitario') * F('items__cantidad'))
            )['total'] or 0
            importe_completados = queryset.filter(estado='completado').aggregate(
                total=Sum(F('items__precio_unitario') * F('items__cantidad'))
            )['total'] or 0

            # Datos para las tarjetas
            extra_context = extra_context or {}
            extra_context.update({
                'cards_doble': True,
                'emoji_1': '🔴',
                'etiqueta_1': 'Pendientes',
                'label_val_etiqueta_1': 'Total:',
                'val_etiqueta_1': f'{pedidos_pendientes}',
                'label_sub_val_etiqueta_1': 'Importe:',
                'sub_val_etiqueta_1': f'$ {importe_pendientes:,.2f}',

                'emoji_2': '💼',
                'etiqueta_2': 'En Proceso',
                'label_val_etiqueta_2': 'Total:',
                'val_etiqueta_2': f'{pedidos_procesando}',
                'label_sub_val_etiqueta_2': 'Importe:',
                'sub_val_etiqueta_2': f'$ {importe_en_preparacion:,.2f}',

                'emoji_3': '🛻',
                'etiqueta_3': 'Por Entregar',
                'label_val_etiqueta_3': f'Terminados: {pedidos_listo}',
                'val_etiqueta_3': f'$ {importe_listo:,.2f}',
                'label_sub_val_etiqueta_3': f'En camino:{pedidos_en_camino}',
                'sub_val_etiqueta_3': f'$ {importe_en_camino:,.2f}',

                'emoji_4': '🚀',
                'etiqueta_4': 'Pedidos Completados',
                'label_val_etiqueta_4': 'Total:',
                'val_etiqueta_4': f'{pedidos_completados}',
                'label_sub_val_etiqueta_4': 'Importe:',
                'sub_val_etiqueta_4': f'$ {importe_completados:,.2f}',
            })

            response.context_data.update(extra_context)

        return response

    def has_add_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return False

    def ACCIONES(self, obj):

        if obj.estado == 'pendiente': 
            return format_html(
                '<a class="btn btn-dark" style="border-radius:5px" href="{}">Confirmar</a>', reverse('confirmar-pedido', args=[obj.id]))
        
        elif obj.estado == 'en_preparacion':
            return format_html(
                '<a class="btn btn-dark" style="border-radius:5px" href="{}">Terminar Armado</a>', reverse('confirmar-armado-pedido', args=[obj.id]))
        
        elif obj.estado == 'listo':
            return format_html(
                '<a class="btn btn-dark" style="border-radius:5px" href="{}">Iniciar Envio</a>', reverse('iniciar-entrega-pedido', args=[obj.id]))
        
        elif obj.estado == 'en_camino':
            return format_html(
                '<a class="btn btn-dark" style="border-radius:5px" href="{}">Finalizar Envio</a>', reverse('finalizar-entrega-pedido', args=[obj.id]))
        





