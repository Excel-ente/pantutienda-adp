from django.contrib import admin
from .models import Mensaje
from django.utils.html import format_html

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'estado_icono', 'creado_en')
    list_filter = ('estado',)
    search_fields = ('usuario__username', 'titulo')

    def estado_icono(self, obj):
        if obj.estado == 'pendiente':
            icono = '⏳'
        elif obj.estado == 'en_proceso':
            icono = '⚙️'
        else:
            icono = '✅'
        return format_html(f'<span>{icono}</span>')
    
    estado_icono.short_description = 'Estado'
