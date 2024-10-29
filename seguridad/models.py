from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone

class FailedLoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    attempt_time = models.DateTimeField(default=timezone.now)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    organizacion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Intento fallido desde {self.ip_address} en {self.attempt_time}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

