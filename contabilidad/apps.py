from django.apps import AppConfig


class ContabilidadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contabilidad'
    
    def ready(self):
        # Importa los signals cuando la app esté lista
        import contabilidad.signals
