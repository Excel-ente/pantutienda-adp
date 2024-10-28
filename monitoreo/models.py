from django.db import models
from django.utils import timezone

class FailedLoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    attempt_time = models.DateTimeField(default=timezone.now)
    user_agent = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)
    request_method = models.CharField(max_length=10, blank=True, null=True)
    referer = models.CharField(max_length=255, blank=True, null=True)
    request_path = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Detectar el tipo de dispositivo de manera básica
        if 'Mobile' in self.user_agent:
            self.device_type = 'Mobile'
        elif 'Tablet' in self.user_agent:
            self.device_type = 'Tablet'
        else:
            self.device_type = 'Desktop'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ip_address} - {self.attempt_time}"
