from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from front.views import custom_logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Redirigir la ruta raíz a 'app/'
    path('', RedirectView.as_view(url='front/home/', permanent=False)), 
        
    # Url del panel de administración
    path('app/', admin.site.urls),
    path('front/', include('front.urls')),
    
    # Ruta para el custom logout
    path('logout/', custom_logout, name='custom_logout'),

    # URLs de modulos
    path('agenda/', include('agenda.urls')),
    path('compras/', include('compras.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('inventario/', include('inventario.urls')),
    path('mensajeria/', include('mensajeria.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
