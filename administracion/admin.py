from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import solicitudEmprendimiento
from import_export.admin import ImportExportModelAdmin
# -----------------------------------------------------------------------------
# Vista proveedor
# 
@admin.register(solicitudEmprendimiento)
class solicitudEmprendimientoAdmin(ImportExportModelAdmin):
    change_list_template = 'change_list.html'
    list_display = ('id','proveedor','emprendimiento','estado',)
    list_filter = ('habilitado',)
    readonly_fields = ('fecha_alta','fecha_habilitacion','habilitado','deshabilitar')
    search_fields = ('proveedor','emprendimiento')

    def deshabilitar(self,obj):
        if obj.habilitado:
            return format_html('<a class="btn btn-danger" style="border-radius:5px" href="{}">Deshabilitar</a>', reverse('deshabilitar-proveedor', args=[obj.id]))
        else:
            return f'-'
        f
    def estado(self, obj):
        if obj.habilitado:
            return f'🟢 Habilitado'
        else:
            return format_html('<a class="btn btn-primary" style="border-radius:5px" href="{}">Autorizar</a>', reverse('autorizar-emprendimiento', args=[obj.id]))
         