from django.db import models
from agenda.models import Proveedor,OnboardingProveedor

# Create your models here.
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class solicitudEmprendimiento(models.Model):
    proveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE,blank=False,null=False)
    emprendimiento = models.ForeignKey(OnboardingProveedor,on_delete=models.CASCADE,blank=False,null=False)
    fecha_alta=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    fecha_habilitacion=models.DateTimeField(blank=True,null=True)
    habilitado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario} | {self.habilitado}'


    def save(self, *args, **kwargs):
        super(Proveedor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'solicitud'
        verbose_name_plural ='🎡 Solicitudes'