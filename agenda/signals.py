from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Cliente  # Importa tu modelo Cliente

@receiver(post_save, sender=User)
def crear_cliente(sender, instance, created, **kwargs):
    if created and instance.is_superuser == False:
        # Si el usuario ha sido creado, crea un Cliente asociado a este usuario
        nuevo_cliente=Cliente.objects.create(
            usuario=instance,
            )
        nuevo_cliente.save()
