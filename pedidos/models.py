from django.db import models
from inventario.models import Producto,ProductoPrecio,Deposito
from agenda.models import Cliente,DireccionEntregaCliente
from django.core.exceptions import ValidationError
from configuracion.envio_mails import send_mail_nuevo_pedido

ESTADO_CHOICES = [
    ('abierto', 'Abierto'),
    ('pendiente', 'Pendiente'),
    ('en_preparacion', 'En preparacion'),
    ('listo', 'Listo'),
    ('en_camino', 'En camino'),
    ('completado', 'Completado'),
    ('cancelado', 'Cancelado'),
]

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion_entrega_cliente = models.ForeignKey(DireccionEntregaCliente, on_delete=models.CASCADE,null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT,verbose_name='Deposito salida',blank=True,null=True,default=1,help_text='Deposito donde saldrá la mercadería.')

    def clean(self):
        if self.estado != 'abierto' and self.estado != 'pendiente':
            raise ValidationError('El pedido no puede modificarse.')
        return super().clean()
    
    # Sobrescribe el método save para detectar nuevos pedidos
    # def save(self, *args, **kwargs):
    #     if self.pk is None and self.estado == 'abierto':
    #         super().save(*args, **kwargs)
    #         send_mail_nuevo_pedido(self)
    #     else:
    #         super().save(*args, **kwargs)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.usuario.username}"

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = '📲 Pedidos'
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,null=True)
    producto_precio = models.ForeignKey(ProductoPrecio, on_delete=models.CASCADE,null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=25,decimal_places=2,blank=False,null=False,default=0)
    subtotal = models.DecimalField(max_digits=25,decimal_places=2,blank=False,null=False,default=0)

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def cantidad_madre(self):
        cantidad = round(float(self.producto_precio.cantidad) * float(self.cantidad),2)
        if self.producto_precio.unidad_de_medida != self.producto.unidad_de_medida:
            if self.producto_precio.unidad_de_medida == "Kilos" or self.producto_precio.unidad_de_medida == "Litros":
                cantidad = float(cantidad) * 1000
            elif self.producto_precio.unidad_de_medida == "Gramos" or self.producto_precio.unidad_de_medida == "Mililitros":
                cantidad = float(cantidad) / 1000
            elif self.producto_precio.unidad_de_medida == "Mts":
                cantidad = float(cantidad) * 100
            elif self.producto_precio.unidad_de_medida == "Cms":
                cantidad = float(cantidad) / 100 
            elif self.producto_precio.unidad_de_medida == "Onzas":
                cantidad = float(cantidad) / 16
            elif self.producto_precio.unidad_de_medida == "Libras":
                cantidad = float(cantidad) * 16  
        return cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido #{self.pedido.id})"

    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto_precio.precio_unitario_calculado()
        super(ItemPedido, self).save(*args, **kwargs)

    def consutlar_stock(self):
        convertir = False
        if self.pedido.estado == 'pendiente':
             
            cant_stock =  float(self.producto.stock_actual)
            cant_solicitada = float(self.producto_precio.cantidad) * float(self.cantidad)
            
            if self.producto_precio.unidad_de_medida != self.producto.unidad_de_medida:
                convertir = True
                if self.producto_precio.unidad_de_medida == "Kilos" or self.producto_precio.unidad_de_medida == "Litros":
                    cant_solicitada = float(cant_solicitada) * 1000
                elif self.producto_precio.unidad_de_medida == "Gramos" or self.producto_precio.unidad_de_medida == "Mililitros":
                    cant_solicitada = float(cant_solicitada) / 1000
                elif self.producto_precio.unidad_de_medida == "Mts":
                    cant_solicitada = float(cant_solicitada) * 100
                elif self.producto_precio.unidad_de_medida == "Cms":
                    cant_solicitada = float(cant_solicitada) / 100 
                elif self.producto_precio.unidad_de_medida == "Onzas":
                    cant_solicitada = float(cant_solicitada) / 16
                elif self.producto_precio.unidad_de_medida == "Libras":
                    cant_solicitada = float(cant_solicitada) * 16     
        
            if cant_solicitada > cant_stock:
                if convertir == True:
                    return f"🔸El stock solicitado es {cant_solicitada} {self.producto.unidad_de_medida}, pero tu stock actual es {self.producto.stock_actual_str}" 
                else:
                    return f"🔸El stock solicitado es {cant_solicitada} {self.producto_precio.unidad_de_medida}, pero tu stock actual es {self.producto.stock_actual_str}" 
            else:
                return f"🔹Listo para confirmar"
        else:
            return f"La consulta de STOCK es para los pedidos pendientes, una vez confirmado no se muestra esta metrica."
        
