# inventario/urls.py
from django.urls import path
from .views import pausar_producto, habilitar_producto

urlpatterns = [
    path('habilitar-producto/<int:id>/', habilitar_producto, name='habilitar-producto'),
    path('pausar-producto/<int:id>/', pausar_producto, name='pausar-producto'),
]
