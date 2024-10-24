from django.urls import path
from .views import *

urlpatterns = [

    # Urls para habilitar/dehabilitar los proveedores
    path('deshabilitar-proveedor/<int:id>/', deshabilitar_proveedor, name='deshabilitar-proveedor'),
    path('habilitar-proveedor/<int:id>/', habilitar_proveedor, name='habilitar-proveedor'),

    # Urls para habilitar/dehabilitar los clientes
    path('deshabilitar-cliente/<int:id>/', deshabilitar_cliente, name='deshabilitar-cliente'),
    path('habilitar-cliente/<int:id>/', habilitar_cliente, name='habilitar-cliente'),

    # Urls para habilitar/dehabilitar los vendedor
    path('deshabilitar-vendedor/<int:id>/', deshabilitar_vendedor, name='deshabilitar-vendedor'),
    path('habilitar-vendedor/<int:id>/', habilitar_vendedor, name='habilitar-vendedor'),

    # Urls para habilitar/dehabilitar los chofer
    path('deshabilitar-chofer/<int:id>/', deshabilitar_chofer, name='deshabilitar-chofer'),
    path('habilitar-chofer/<int:id>/', habilitar_chofer, name='habilitar-chofer'),

]
