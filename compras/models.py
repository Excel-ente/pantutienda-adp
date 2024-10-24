from django.db import models
from django.utils import timezone
from inventario.models import Deposito,Producto,ProductoPrecio
from agenda.models import Flota, OnboardingProveedor, Vendedor,Chofer,Proveedor
from configuracion.models import configuracion
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Compra(models.Model):
    fecha = models.DateField(default=timezone.now)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT,blank=True,null=True, help_text='Si no selecciona proveedor, la compra se mostrará como "Proveedores Generales"')
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT,verbose_name='Deposito ingreso',blank=False,null=False,default=1,help_text='Seleccione el deposito donde ingresará la mercadería.')
    total = models.DecimalField(max_digits=25,decimal_places=2,blank=False,null=False,default=0)
    estado = models.BooleanField(default=False)

    en_transito = models.BooleanField(default=False)
    en_descarga = models.BooleanField(default=False)
    descargas = models.IntegerField(default=0)
    compra_inicial = models.BooleanField(default=False)

    observacion = models.TextField(blank=True,null=True,verbose_name='Observaciones')

    detalle=models.TextField(blank=True,null=True,help_text='Campo generado automáticamente por el sistema.')

    anulada = models.BooleanField(default=False)
    anulada_el = models.DateTimeField(blank=True,null=True)
    anulada_por = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)

    class Meta:
        verbose_name = 'compra'
        verbose_name_plural = '📥 Orden de compra'

    def __str__(self):
        moneda = configuracion.objects.first().Moneda
        if self.proveedor:
            return f'OC | {self.fecha} - {self.proveedor.usuario} | {moneda} {self.total_compra():,.2f}'
        else:
            return f'OC | {self.fecha} - Compras Generales | {moneda} {self.total_compra():,.2f}'
     
    def clean(self):
        if self.estado == True:
            raise ValidationError("La orden de compra se encuentra confirmada. No se puede modificar.")
        super().clean()
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.total =  self.total_compra()
            self.detalle = self.calcular_resultado_compra()
        super(Compra, self).save(*args, **kwargs)
    
    def calcular_resultado_compra(self):
        """Calcula la variación porcentual entre el costo actual y el anterior."""
        total_anterior = 0
        total_actual = 0

        detalles = detalleCompra.objects.filter(compra=self)
        for detalle in detalles:
            total_anterior += detalle.producto.costo_unitario * detalle.cantidad
            total_actual += detalle.total

        if total_anterior == 0:
            return "Compra inicial. No hay comparación disponible."

        diferencia = ((total_actual - total_anterior) / total_anterior) * 100
        if diferencia > 0:
            return f"La compra es un {diferencia:.2f}% más cara que la anterior."
        elif diferencia < 0:
            return f"La compra es un {abs(diferencia):.2f}% más barata que la anterior."
        else:
            return "No hay diferencia de costo con respecto a la compra anterior."


    def total_flete(self):
        total = float(0)
        fletes = FleteCompra.objects.filter(compra=self)
        if fletes:
            for flete in fletes:
                total += float(flete.importe)
   
        return total
    
    def total_nc(self):
        total = float(0)
        nc = NotaDeCreditoCompra.objects.filter(compra=self)
        if nc:
            total -= float(nc.first().total_nc())
        return total

    def total_compra(self):

        total = float(self.total_flete())
        total += float(self.total_nc())

        detalles = detalleCompra.objects.filter(compra=self)
        if detalles:
            for detalle in detalles:
                total += float(detalle.total)

        return total
        
    def nc_asociada(self):
        nc = NotaDeCreditoCompra.objects.filter(
            compra=self
        )
        if nc:
            return nc
        else:
            return False

class FleteCompra(models.Model):
    compra=models.ForeignKey(Compra,on_delete=models.CASCADE)
    importe =models.DecimalField(max_digits=25,decimal_places=2,default=0)
    chofer=models.ForeignKey(Chofer,on_delete=models.SET_NULL,blank=True,null=True)
    vehiculo=models.ForeignKey(Flota,on_delete=models.SET_NULL,blank=True,null=True)
    direccion_retiro = models.ForeignKey(OnboardingProveedor,on_delete=models.SET_NULL,blank=True,null=True)
    direccion_descarga = models.ForeignKey(Deposito,on_delete=models.SET_NULL,blank=True,null=True)
    ruta_maps = models.URLField(max_length=255, null=True, blank=True)
    comentarios=models.TextField(blank=True,null=True)
    cancelado = models.BooleanField(default=False)

    def clean(self):
        if self.importe > 0 and not self.chofer:
            raise ValidationError("Debe seleccionar un chofer.")
        super().clean()

    def save(self, *args, **kwargs):
        """Genera automáticamente el link de 'Cómo llegar'."""
        if self.direccion_retiro and self.direccion_descarga:
            origen = self.direccion_retiro.direccion.replace(' ', '+')
            destino = self.direccion_descarga.direccion.replace(' ', '+')
            self.ruta_maps = f"https://www.google.com/maps/dir/?api=1&origin={origen}&destination={destino}"
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'flete'
        verbose_name_plural = '🚚 Fletes'

class NotaDeCreditoCompra(models.Model):
    fecha = models.DateField(default=timezone.now)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE,blank=False,null=False,default=1,verbose_name='compra')
    motivo = models.CharField(max_length=255,blank=False,null=False)
    estado = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)

    anulada = models.BooleanField(default=False)
    anulada_el = models.DateTimeField(blank=True,null=True)
    anulada_por = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    
    class Meta:
        verbose_name = 'Nota de credito'
        verbose_name_plural = '📕 Notas de credito'

    def __str__(self):
        moneda = configuracion.objects.first().Moneda
        if self.compra.proveedor.Empresa:
            return f'NC | {self.fecha} - {self.compra.proveedor.Empresa} {self.compra.proveedor.NombreApellido}| {moneda} {self.total_nc():,.2f}'
        else:
            return f'NC | {self.fecha} - {self.compra.proveedor.NombreApellido} | {moneda} {self.total_nc():,.2f}'
     
    def clean(self):
        if self.estado == True:
            raise ValidationError("La nota de crédito se encuentra confirmada. No se puede modificar.")
        
        
        super().clean()
    
      
    def save(self, *args, **kwargs):
        super(NotaDeCreditoCompra, self).save(*args, **kwargs)


    def total_nc(self):
        total = 0
        # detalles = detalleNotaCredito.objects.filter(NotaCredito=self)
        # for detalle in detalles:
        #     total += detalle.Subtotal()
        return total
 
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# productoprecio.precio_unitario()    ---> Devuelve el precio de venta unitario
# productoprecio.precio_total()    ---> Devuelve el precio de venta total
# productoprecio.costo_total()    ---> Devuelve el costo final de venta del producto
class detalleCompra(models.Model):
    fecha = models.DateField(auto_now_add=True)
    compra = models.ForeignKey('compras.Compra', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=25, decimal_places=3,default=1)
    precio = models.DecimalField(max_digits=25,decimal_places=3,default=0)
    descuento = models.DecimalField(verbose_name="Desc (%)",max_digits=5, decimal_places=2,default=0)
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE,verbose_name='Deposito ingreso',blank=False,null=False)
    total = models.DecimalField(max_digits=25,decimal_places=2,default=0,blank=False,null=False)
    ActualizarCosto = models.BooleanField(default=True)
    detalle=models.TextField(blank=True,null=True,help_text='Campo generado automáticamente por el sistema.')

    class Meta:
        verbose_name = 'detalle de compra'
        verbose_name_plural = '📦 Productos comprados'

        # Evita productos duplicados en la base de datos (nivel de DB opcional)
        unique_together = ('compra', 'producto')

    @property
    def precio_calculado(self):
        descuento = float(self.precio) * float(self.descuento) / 100
        precio= (float(self.precio) - float(descuento))
        return precio
    
    @property
    def total_calculado(self):
        descuento = float(self.precio) * float(self.descuento) / 100
        precio= (float(self.precio) - float(descuento)) * float(self.cantidad)
        return precio
    
    def clean(self):

        tipo_descuento = 0
        if tipo_descuento == 0:
            if self.descuento > 100:
                raise ValidationError("El descuento no puede ser superior a 100%.")
            if self.descuento < 0:
                raise ValidationError("El descuento debe ser superior o igual a 0%.")
                
        super().clean()
    

    def save(self, *args, **kwargs):

        # tipo de descuento 0 es en % y 1 es para que sea por importe.
        tipo_descuento = 0

        if tipo_descuento == 0:
            precio = float(self.precio)
            descuento = (precio * float(self.descuento) / 100)
            self.total = float(precio - descuento) * float(self.cantidad)
        else:
            self.total = float((self.precio * self.cantidad) - self.descuento)
        
        try:
            self.deposito = self.compra.deposito
        except:
            pass    

        self.detalle = self.detalle_compra()

        super(detalleCompra, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'detalle de comrpa'
        verbose_name_plural = '📦 Productos comprados' 

    # def compras_mensual(fecha_inicial, fecha_final):
        # from compra.models import Compra
        # from django.db.models import Sum, F, ExpressionWrapper, DecimalField

        # # Obtener las ventas por día
        # compras_por_dia = Compra.objects.filter(
        #     fecha__range=(fecha_inicial, fecha_final),
        #     estado=True
        # ).values('fecha').annotate(total=Sum(ExpressionWrapper(F('total'), output_field=DecimalField())))

        # # Sumar los valores de total_venta
        # total = sum(venta['total'] for venta in compras_por_dia)
        
        # return total
    
    def costo_unitario(self):
        costo_unitario = float(self.total) / float(self.cantidad)
        return costo_unitario
    
    def resultado_compra(self):
        valor = 0
        costo_anterior = float(self.producto.costo_unitario)
        costo_nuevo = float(self.precio_calculado)
        if costo_anterior == 0:
            pass
        else:
            valor = ((costo_nuevo - costo_anterior) / costo_anterior) * 100
        return valor

    def detalle_compra(self):
        config = configuracion.objects.first()
        costo_anterior = float(self.producto.costo_unitario)
        costo_nuevo = float(self.precio_calculado)
        if costo_anterior == 0:
            if self.total_calculado > 0:
                return f'El aumento respecto al último costo es % 100.'
            else:
                return f'Sin cambios registrados'
        else:
            dif = ((costo_nuevo - costo_anterior) / costo_anterior) * 100
            if dif > 0:
                return f'Esta compra está por un % {dif:,.2f} sobre el ultimo costo. (Ultimo costo registrado: {config.Moneda.signo} {self.producto.costo_unitario:,.2f})'
            elif round(dif,0) == 0:
                return f'Sin diferencia respecto al último costo registrado.'
            else:
                return f'Esta compra está por un % {dif:,.2f} debajo del ultimo costo. (Ultimo costo registrado: {config.Moneda.signo} {self.producto.costo_unitario:,.2f})'

    def presentacion(self):
        presentaciones = ProductoPrecio.objects.filter(producto=self.producto).order_by('-cantidad')
        unidades_compradas = int(self.cantidad)
        
        resultado = []
        for presentacion in presentaciones:
            unidades_por_presentacion = presentacion.cantidad
            if unidades_compradas >= unidades_por_presentacion:
                cantidad = unidades_compradas // unidades_por_presentacion
                unidades_compradas %= unidades_por_presentacion
                resultado.append(f'{cantidad} {presentacion.presentacion.nombre}')
        
        if unidades_compradas > 0:
            resultado.append(f'{unidades_compradas} unidades')

        return ' y '.join(resultado)
