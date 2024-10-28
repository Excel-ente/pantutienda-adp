from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Pedido
from configuracion.envio_mails import send_mail_nuevo_pedido,send_mail_pedido_confirmado

# Variable para almacenar el estado previo
@receiver(pre_save, sender=Pedido)
def almacenar_estado_anterior(sender, instance, **kwargs):
    if instance.pk:
        # Obtiene el estado anterior desde la base de datos
        instance._estado_anterior = Pedido.objects.get(pk=instance.pk).estado
    else:
        # Si el pedido es nuevo, no tiene estado anterior
        instance._estado_anterior = None

# Señal post_save para enviar el correo después de confirmar el pedido
@receiver(post_save, sender=Pedido)
def enviar_correo_confirmacion(sender, instance, created, **kwargs):
    # Solo envía el correo cuando el pedido cambia de 'abierto' a 'pendiente'
    if instance._estado_anterior == 'abierto' and instance.estado == 'pendiente':
        send_mail_nuevo_pedido(instance)

    elif instance._estado_anterior == 'pendiente' and instance.estado == 'en_preparacion':    
        send_mail_pedido_confirmado(instance)