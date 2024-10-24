from django.urls import path
from .views import *


urlpatterns = [
    path('descargar_excel/<int:id_compra>/', descargar_excel, name='descargar_excel'),
    path('popup_comparar_productos/<int:id_compra>/', popup_comparar_productos, name='popup_comparar_productos'),
    path('ver_google_maps/<int:id_flete>/', ver_google_maps, name='ver_google_maps'),
    # Urls para la gestion de compra
    path('confirmar-compra/<int:id>/', confirmar_compra, name='confirmar_compra'),
    path('iniciar-descarga/<int:id>/', iniciar_descarga, name='iniciar_descarga'),
    path('terminar-descarga/<int:id>/', terminar_descarga, name='terminar_descarga'),
]

