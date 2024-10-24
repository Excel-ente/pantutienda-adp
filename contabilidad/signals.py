from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Cuentas)
def asignar_numero_cuenta(sender, instance, created, **kwargs):
    if created and instance.numero is None:
        instance.numero = instance.id
        instance.save()

@receiver(post_save, sender=CuentasComerciales)
def asignar_numero_cuenta_comercial(sender, instance, created, **kwargs):
    if created and instance.numero is None:
        instance.numero = instance.id
        instance.save()
