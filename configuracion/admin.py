from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import *


# -----------------------------------------------------------------------------
# Vista TipoCliente
@admin.register(configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('emprendimiento',)
    exclude =('mail_bienvenida_proveedor','mail_bienvenida_cliente')


    def has_add_permission(self, request, obj=None):
        # Disables the ability to add new records directly in the admin
        return True

    def has_change_permission(self, request, obj=None):
        # Disables the ability to change existing records directly in the admin
        return True

    def has_delete_permission(self, request, obj=None):
        # Allows the ability to delete records in the admin
        return True

# -----------------------------------------------------------------------------
# Vista TipoCliente
@admin.register(TipoCliente)
class TipoClienteAdmin(ImportExportModelAdmin):
    list_display = ('descripcion',)


# -----------------------------------------------------------------------------
# Vista Monedas
# 
@admin.register(Monedas)
class MonedasAdmin(ImportExportModelAdmin):
    list_display = ('nombre','abreviacion','signo')


# -----------------------------------------------------------------------------
# Vista medioDeCompra
# 
@admin.register(medioDeCompra)
class medioDeCompraAdmin(ImportExportModelAdmin):
    list_display = ('nombre','moneda',)
    readonly_fields = ('moneda',)

 
# -----------------------------------------------------------------------------
# Vista medioDeVenta
# 
@admin.register(medioDeVenta)
class medioDeVentaAdmin(ImportExportModelAdmin):
    list_display = ('nombre','moneda',)
    readonly_fields = ('moneda',)


# -----------------------------------------------------------------------------
# Vista ListaDePrecio
# 
@admin.register(ListaDePrecio)
class ListaDePrecioAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)
    list_per_page = 15

