from django.db import models
from django.utils import timezone
from agenda.models import *
from .utils import obtener_saldo_cuenta,obtener_saldo_cuenta_comercial
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from .listas import *

class CuentasComerciales(models.Model):
    numero = models.IntegerField(unique=True,blank=True,null=True)
    descripcion = models.CharField(max_length=120,null=True,blank=True)
    moneda = models.ForeignKey('configuracion.Monedas',on_delete=models.PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, null=True, blank=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'cuenta'
        verbose_name_plural ='🪪 Cuentas comerciales' 

    @property
    def saldo_actual(self):
        saldo=obtener_saldo_cuenta_comercial(self)
        return saldo

    def __str__(self):
        if self.cliente:
            return f'{self.cliente} | Saldo: {self.moneda} {self.saldo_actual:,.2f}'
        elif self.chofer:
            return f'{self.chofer} | Saldo: {self.moneda} {self.saldo_actual:,.2f}'
        elif self.vendedor:
            return f'{self.vendedor} | Saldo: {self.moneda} {self.saldo_actual:,.2f}'
        else:
            return f'{self.proveedor} | Saldo: {self.moneda} {self.saldo_actual:,.2f}'
        
    def clean(self): 
        return super().clean()

class Cuentas(models.Model):
    numero = models.IntegerField(unique=True,blank=True,null=True)
    moneda = models.ForeignKey('configuracion.Monedas',on_delete=models.PROTECT,null=True,blank=True)
    descripcion = models.CharField(max_length=120,null=True,blank=True)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA,default='Activo', null=False, blank=False)

    def __str__(self):
        if self.tipo_cuenta == 'Personal':
            return f'Cuenta de {self.usuario} | {self.descripcion} | Saldo: {self.moneda} {self.saldo_actual:,.2f}'
        elif self.tipo_cuenta == 'Punto de Venta':
            return f'Caja: {self.punto_de_venta} | Saldo: {self.moneda} {self.saldo_actual:,.2f}'
        else:
            tipo=self.tipo_cuenta
            return f'{self.descripcion} ({tipo}) | Saldo: {self.moneda} {self.saldo_actual:,.2f}'
        
    def clean(self): 
        return super().clean()
    
    class Meta:
        verbose_name = 'cuenta'
        verbose_name_plural ='💼 Cuentas Patrimoniales' 

    @property
    def saldo_actual(self,):
        saldo=obtener_saldo_cuenta(self)
        return saldo

class Asientos(models.Model):
    fecha = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=35,choices=TIPO_MOVIMIENTO,default='Patrimonial',null=False,blank=False)
    detalle = models.CharField(max_length=120,null=True,blank=True)
    estado = models.BooleanField(default=False)

    def clean(self): 
        return super().clean()
    
    def __str__(self):
        return f'{self.pk}'
    
    class Meta:
        verbose_name = 'asiento'
        verbose_name_plural ='📇 Asientos' 
 
class MovimientosCuentaContable(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    asiento = models.ForeignKey(Asientos, on_delete=models.CASCADE, null=False, blank=False)
    cuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE, null=True, blank=True)
    debe = models.DecimalField(max_digits=25, decimal_places=2,default=0 ,blank=False,null=False)
    haber = models.DecimalField(max_digits=25, decimal_places=2,default=0 ,blank=False,null=False)
    comentarios = models.CharField(max_length=255,blank=True,null=True)

    def clean(self): 
        return super().clean()
    
    def __str__(self):
        return f'Precio {self.pk}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.fecha = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'movimiento'
        verbose_name_plural ='📚 Movimientos' 

    def saldo_cuenta(self,cuenta_select):
        saldo = Cuentas.objects.filter(cuenta=cuenta_select)
        debe = saldo.sum('debe')
        haber = saldo.sum('haber')
        return debe - haber

class MovimientosCuentaComercial(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    asiento = models.ForeignKey(Asientos, on_delete=models.CASCADE, null=False, blank=False)
    cuenta = models.ForeignKey(CuentasComerciales, on_delete=models.CASCADE, null=True, blank=True)
    debe = models.DecimalField(max_digits=25, decimal_places=2,default=0 ,blank=False,null=False)
    haber = models.DecimalField(max_digits=25, decimal_places=2,default=0 ,blank=False,null=False)
    comentarios = models.CharField(max_length=255,blank=True,null=True)

    def clean(self): 
        return super().clean()
    
    def __str__(self):
        return f'Precio {self.pk}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.fecha = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'movimiento'
        verbose_name_plural ='📚 Movimientos' 

    def saldo_cuenta(self,cuenta_select):
        saldo = CuentasComerciales.objects.filter(cuenta=cuenta_select)
        debe = saldo.sum('debe')
        haber = saldo.sum('haber')
        return debe - haber