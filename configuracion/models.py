from django.db import models
from contabilidad.models import Cuentas
from .listas import *
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from agenda.models import Proveedor

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class Monedas(models.Model):
    '''
        monedas utilizables
    '''
    nombre = models.CharField(max_length=255,unique=True,blank=False,null=False,default="Pesos")
    abreviacion = models.CharField(max_length=3,unique=True,blank=False,null=False,default="ARS")
    signo = models.CharField(max_length=5,blank=True,null=True,default="$")
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.abreviacion}'

    class Meta:
        verbose_name = 'moneda'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='🪙 Monedas' # Como se nombra el modelo

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class medioDeCompra(models.Model):
    '''
        modelo para registrar el metodo de pago de las compras que hacen los proveedores.
        ::
        esta tabla solo sera de uso para los proveedores.
    '''
    nombre = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.CharField(max_length=50,choices=TIPO_MDP,blank=False,null=False,default="Efectivo")
    cuenta = models.ForeignKey(Cuentas,on_delete=models.CASCADE,blank=False,null=True)
    moneda = models.ForeignKey(Monedas,on_delete=models.CASCADE,blank=False,null=True)

    def clean(self): 
        super().clean()
        
    def save(self, *args, **kwargs):
  
        if self.cuenta.punto_de_venta:
            self.moneda = self.cuenta.moneda
        super().save(*args, **kwargs)

    def __str__(self): 
        return f'{self.moneda} | {self.Nombre}'
    
    class Meta: # Metodo para nombrar el modelo
        verbose_name = 'medio de compra'  # Como se va a nombrar el objeto de la instancia
        verbose_name_plural ='💸 MDP Compras' # Como se nombra el modelo

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class medioDeVenta(models.Model):
    '''
        modelo para registrar el metodo de pago de las ventas (pedidos) que hacen los clientes.
    
    '''
    nombre = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.CharField(max_length=50,choices=TIPO_MDP,blank=False,null=False,default="Efectivo")
    cuenta = models.ForeignKey(Cuentas,on_delete=models.CASCADE,blank=False,null=True)
    moneda = models.ForeignKey(Monedas,on_delete=models.CASCADE,blank=False,null=True)

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
  
        if self.cuenta.punto_de_venta:
            self.punto_de_venta = self.cuenta.punto_de_venta
            self.moneda = self.cuenta.moneda
        super().save(*args, **kwargs)

    def __str__(self): 
        return f'{self.punto_de_venta} | {self.Nombre}'
    
    class Meta: 
        verbose_name = 'medio de pago'
        verbose_name_plural ='🪙 MDP Ventas' 

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class TipoCliente(models.Model):
    descripcion = models.CharField(max_length=255,unique=True,blank=False,null=False)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name = 'tipo cliente' 
        verbose_name_plural ='💼 Tipo de clientes' 

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class ListaDePrecio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'lista'
        verbose_name_plural = '📒 Listas de Precios'

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class configuracion(models.Model):
    '''
        este modelo lo utiilizamos para todas las configuraciones del emprendimiento
    '''
    emprendimiento = models.CharField(max_length=255,blank=True,null=True)
    Moneda = models.ForeignKey(Monedas, on_delete=models.SET_NULL, blank=True, null=True, related_name='moneda_principal')
    Moneda_secundaria = models.ForeignKey(Monedas, on_delete=models.SET_NULL, blank=True, null=True, related_name='moneda_secundaria')
    tipo_cambio_1 = models.DecimalField(max_digits=25, decimal_places=10, default=1, blank=False, null=False)
    calculo_rentabilidad = models.CharField(max_length=50,choices=RENTABILIDAD,blank=False,null=False,default="Sobre costo")
    gastos_fletes_compras = models.CharField(max_length=50,choices=FLETES_COMPRAS_CHOICES,blank=False,null=False,default="Distribuir costo en productos",help_text='Si usted desea que el gasto del flete al hacer la compra se distribuya entre los productos comprados (Actualiza costo tomando el flete), Debe seleccionar "Distribuir costo en productos", en caso contrario el gasto del flete irá a la cuenta de GASTOS VARIOS.')
    venta_stock_negativo = models.BooleanField(default=False,help_text='Si desea vender sin limites de inventario, deje esta casilla en Verdadero. (Genera Stock Negativo)')
    valuar_stock_negativo = models.BooleanField(default=False,help_text='Si desea que el stock negativo reste de su valuacion, deje esta casilla en Verdadero.')
    precio_venta_automatico = models.BooleanField(default=False,verbose_name='Precio venta basado en rentabilidad',help_text='Si desea que el precio de venta del producto se calcule en base a una rentabilidad sobre el costo, deje esta casilla en Verdadero. En el caso contrario, se habilitará una casilla para colocar el precio final de venta.')
    unidad_de_medida_precio_venta = models.BooleanField(default=False,help_text='Permite Modificar la unidad de medida del precio del producto')
    confirmar_viaje_compra = models.BooleanField(default=True,help_text='Esta opcion permite al usuario confirmar cuando la compra llega al deposito de ingreso. [🚚 llegada]')
    confirmar_descarga_compra = models.BooleanField(default=True,help_text='Esta opcion permite al usuario confirmar cuando la mercaderia se ingresó correctamente a inventario. [📦 Iniciar descarga]')
    confirmar_pisar_costo = models.BooleanField(default=True,help_text='Si desea actualizar el costo unitario de forma automática según la ultima compra, deje esta casilla en Verdadero. (En falso, se muestra casilla ✔️ Actualizar Costo en producto comprado)')
    editar_fecha_compra = models.BooleanField(default=False,help_text='Si desea poder editar la fecha en la compra, deje esta casilla en Verdadero.')
    limite_pedidos_pendientes = models.PositiveIntegerField(default=2,blank=False,null=False)
    mail_bienvenida_cliente = models.BooleanField(default=False)
    mail_bienvenida_proveedor = models.BooleanField(default=False)
    gestionar_armar_pedido = models.BooleanField(default=False,help_text='Si desea gestionar el armado de los pedidos, dejar esta casilla en True.')
    gestionar_entrega = models.BooleanField(default=False,help_text='Si desea gestionar la entrega de los pedidos de clientes (Fletes, Entregas), dejar esta casilla en True.')
    
    class Meta:
        verbose_name = 'configuracion' 
        verbose_name_plural ='⚙️ Configuracion'
        
    def clean(self):
        super().clean()




