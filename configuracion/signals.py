from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import configuracion
from inventario.models import ProductoPrecio

@receiver(post_save, sender=configuracion)
def recalculate_prices(sender, instance, **kwargs):
    # Obtiene todos los registros de ProductoPrecio y recalcula los precios
    for precio in ProductoPrecio.objects.all():
        precio.precio_unitario = precio.precio_unitario_calculado()
        precio.precio_total = precio.precio_unitario * precio.cantidad
        precio.save()
