from django.urls import path
from .views import *

urlpatterns = [
    path('carrito/', carrito, name='carrito'),
    path('carrito/agregar/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/', actualizar_carrito, name='actualizar_carrito'),  # Sin item_id
    path('carrito/eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),

    path('confirmar-pedido/<int:id>/', confirmar_pedido, name='confirmar-pedido'),
    path('confirmar-armado-pedido/<int:id>/', confirmar_armado_pedido, name='confirmar-armado-pedido'),
    path('iniciar-entrega-pedido/<int:id>/', iniciar_armado_pedido, name='iniciar-entrega-pedido'),
    path('finalizar-entrega-pedido/<int:id>/', finalizar_armado_pedido, name='finalizar-entrega-pedido'),
]


