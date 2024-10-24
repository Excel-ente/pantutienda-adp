from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('home/', home, name='home'),
    path('productos/', productos, name='productos'),
    path('carrito/', carrito, name='carrito'),
    path('registro/', registro, name='registro'),
    path('login/', custom_login, name='login'),
    path('cuenta-no-verificada/', cuenta_no_verificada, name='cuenta_no_verificada'),
    path('pedidos/', pedidos_view, name='pedidos_view'), 
    path('confirmar-pedido/', confirmar_pedido, name='confirmar_pedido_view'),
    path('cambiar-clave/', change_password, name='change_password'),
]


