from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import detalleCompra, Compra

@receiver([post_save, post_delete], sender=detalleCompra)
def actualizar_total_compra(sender, instance, **kwargs):
    """Actualiza el total de la compra cada vez que un detalle se guarda o elimina."""
    compra = instance.compra
    total = compra.total_compra() or 0
    compra.total = total
    compra.save()
