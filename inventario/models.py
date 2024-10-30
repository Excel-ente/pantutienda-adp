from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from configuracion.models import *
from .listas import *
from .utils import convertir_unidad
from django.db.models import Sum
from agenda.models import Proveedor
import os
from django.conf import settings

def validate_image_size(value):
    width, height = value.width, value.height
    if width != 500 or height != 500:
        raise ValidationError('La imagen debe ser de 500x500 píxeles.')
    
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class Deposito(models.Model): # ok
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255,blank=True,null=True)
    telefono = models.CharField(max_length=255,blank=True,null=True)
    pin_maps = models.URLField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f'Deposito: {self.nombre} | Direccion: {self.direccion}'

    class Meta:
        verbose_name = 'deposito'
        verbose_name_plural = '🏭 Depositos'

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(
        upload_to='img/landing/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), validate_image_size]
    )

    def __str__(self):
        return self.nombre


        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = '📚 Categorias'

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class Presentacion(models.Model):
    nombre = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'presentacion'
        verbose_name_plural = '🍶 Presentacion'

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# producto.stock_actual()    ---> Devuelve la cantidad de productos en stock disponibles para venta (decimal)
# producto.stock_actual_str()    ---> Devuelve la cantidad de productos en stock disponibles para venta con la unidad de medida (string)
# producto.pedidos_encurso()    ---> Devuelve la cantidad de pedidos en curso de clientes asociados al vendedor
# producto.pedidos_pendientes()    ---> Devuelve la cantidad de pedidos pendientes de clientes asociados al vendedor

class Producto(models.Model):
    codigo = models.CharField(max_length=100,blank=True,null=True)
    nombre = models.CharField(max_length=100,blank=False,null=False)
    descripcion = models.CharField(max_length=200,blank=True,null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='Simple')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    unidad_de_medida = models.CharField(max_length=50,choices=UNIDADES_DE_MEDIDA,blank=False,null=False,default="Unidades")
    costo_unitario = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Proveedor Ult. Compra')

    imagen = models.ImageField(
        max_length=255,
        upload_to='img/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), validate_image_size]
    )

    habilitar_venta = models.BooleanField(default=False)
    ultima_modificacion = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = '📦 Productos'

    def __str__(self):
        return f'{self.nombre}'
    
    def save(self, *args, **kwargs):
        if self.tipo == 'Compuesto':
            self.costo_unitario = self.costo_unitario_calculado()

        super().save(*args, **kwargs)

    def es_publicable(self):
        if ProductoPrecio.objects.filter(producto=self):
            return True
        else:
            return False

    # Función para calcular el costo total si el producto es compuesto
    def calcular_costo_total(self):
        if self.tipo == 'Compuesto':
            # Sumar el costo de los productos en la receta
            return sum([
                receta.cantidad * receta.producto_usado.costo_unitario
                for receta in self.recetas.all()
            ])
        return self.costo_unitario
        
    @property
    def stock_actual(self):

        entradas_sum = MovimientoProducto.objects.filter(
            producto=self
        ).aggregate(total_entradas=Sum('entrada'))['total_entradas'] or 0

        salidas_sum = MovimientoProducto.objects.filter(
            producto=self
        ).aggregate(total_salidas=Sum('salida'))['total_salidas'] or 0
        
        mermas = Merma.objects.filter(
            producto=self
        ).aggregate(total=Sum('cantidad'))['total'] or 0
           
        stock_actual = entradas_sum - salidas_sum - mermas
        return stock_actual
    
    @property
    def stock_actual_str(self):
        moneda = configuracion.objects.first().Moneda.signo
        return f'{self.stock_actual:,.2f} {self.unidad_de_medida[:3]} ({moneda} {self.valuacion_stock:,.2f})' 
    
    @property
    def primer_producto_precio(self):
        return ProductoPrecio.objects.filter(producto=self).first()
    
    @property
    def productos_precio(self):
        return ProductoPrecio.objects.filter(producto=self)

    @property
    def valuacion_stock(self):
        stock=float(self.stock_actual)
        valuar_negativos = configuracion.objects.first().valuar_stock_negativo
        valuacion = float(stock) * float(self.costo_unitario)
        if valuar_negativos==False:
            if stock < 0:
                valuacion = 0 
        return valuacion
    
    @property
    def valuacion_stock_negativo(self):
        stock=float(self.stock_actual)
        if stock < 0:
            valuacion = float(stock) * float(self.costo_unitario)
        else:
            valuacion=0
        return valuacion
    
    def costo_unitario_calculado(self):
        
        if self.tipo == 'Compuesto':
            # Obtener todos los ingredientes asociados al producto a través de la receta
            ingredientes = RecetaProducto.objects.filter(producto_principal=self)
            
            # Calcular el costo total en base a cada ingrediente y su cantidad
            costo_total = sum(ingrediente.Costo_calculado() for ingrediente in ingredientes)
   
            return costo_total
        
        return self.costo_unitario
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# productoprecio.precio_unitario()    ---> Devuelve el precio de venta unitario
# productoprecio.precio_total()    ---> Devuelve el precio de venta total
# productoprecio.costo_total()    ---> Devuelve el costo final de venta del producto
class RecetaProducto(models.Model):
    producto_principal = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas')
    producto_usado = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='usado_en_recetas')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_de_medida = models.CharField(max_length=50, choices=UNIDADES_DE_MEDIDA)

    def __str__(self):
        return f'{self.cantidad} {self.unidad_de_medida} de {self.producto_usado.nombre}'
    
    class Meta:
        verbose_name = 'composicion'
        verbose_name_plural = '🛠️ Composicion'

    def Costo_calculado(self):
        costo_unitario = float(self.producto_usado.costo_unitario) * float(self.cantidad) or 0
        if self.unidad_de_medida != self.producto_usado.unidad_de_medida:
            if self.unidad_de_medida == "Kilos" or self.unidad_de_medida == "Litros":
                costo_unitario = float(costo_unitario) * 1000
            elif self.unidad_de_medida == "Gramos" or self.unidad_de_medida == "Mililitros":
                costo_unitario = float(costo_unitario) / 1000
            elif self.unidad_de_medida == "Mts":
                costo_unitario = float(costo_unitario) * 100
            elif self.unidad_de_medida == "Cms":
                costo_unitario = float(costo_unitario) / 100 
            elif self.unidad_de_medida == "Onzas":
                costo_unitario = float(costo_unitario) / 16
            elif self.unidad_de_medida == "Libras":
                costo_unitario = float(costo_unitario) * 16    

        return costo_unitario

    def clean(self): 
        if self.validad_udm() != True:
            raise ValidationError(f"Validar Unidad de medida.") 
        return super().clean()
    
    def validad_udm(self):
        '''
            Esta validacion es para ver si las unidades de medida corresponden.
            Solo se usa al guardar un precio de producto
        '''
        unidad_compra=self.producto_usado.unidad_de_medida
        unidad_uso=self.unidad_de_medida
        if unidad_compra==unidad_uso:
            return True
        else: 
            if unidad_compra == 'Unidades':
                raise ValidationError(f"El precio tiene que tener la siguiente unidad de medida: Unidades")
            elif unidad_compra == 'Mt2s':
                raise ValidationError(f"El precio tiene que tener la siguiente unidad de medida: Mt2s")
            elif unidad_compra == 'Kilos':
                if unidad_uso != 'Gramos':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Kilos o Gramos")
            elif unidad_compra == 'Gramos':
                if unidad_uso != 'Kilos':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Kilos o Gramos")
            elif unidad_compra == 'Litros':    
                if unidad_uso != 'Mililitros':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Litros o Mililitros")
            elif unidad_compra == 'Mililitros':
                if unidad_uso != 'Litros':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Litros o Mililitros")
            elif unidad_compra == 'Onzas':    
                if unidad_uso != 'Libras':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Libras o Onzas")
            elif unidad_compra == 'Libras':
                if unidad_uso != 'Onzas':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Libras o Onzas")
            elif unidad_compra == 'Mts':    
                if unidad_uso != 'Cms':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Mts o Cms")
            elif unidad_compra == 'Cms':
                if unidad_uso != 'Mts':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Mts o Cms")
            return True

# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
# productoprecio.precio_unitario()    ---> Devuelve el precio de venta unitario
# productoprecio.precio_total()    ---> Devuelve el precio de venta total
# productoprecio.costo_total()    ---> Devuelve el costo final de venta del producto
class ProductoPrecio(models.Model):
    lista = models.ForeignKey(ListaDePrecio,on_delete=models.CASCADE,null=True,blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    presentacion = models.ForeignKey(Presentacion,on_delete=models.CASCADE,blank=False,null=True)
    cantidad = models.IntegerField(default=1)
    rentabilidad = models.DecimalField(max_digits=5, decimal_places=2,default=0 ,blank=False,null=False)
    precio_manual = models.DecimalField(max_digits=20, decimal_places=2,default=0 ,blank=False,null=False)
    unidad_de_medida = models.CharField(max_length=50,choices=UNIDADES_DE_MEDIDA,blank=False,null=False,default="Unidades")
    precio_unitario = models.DecimalField(max_digits=20, decimal_places=2,default=0 ,blank=False,null=False)
    precio_total = models.DecimalField(max_digits=20, decimal_places=2,default=0 ,blank=False,null=False)

    def __str__(self):
        return f'{self.producto} x {self.presentacion} ({self.cantidad} {self.unidad_de_medida}) $ {self.precio_unitario:,.2f}'
    

    def clean(self): 

        config = configuracion.objects.first().calculo_rentabilidad
        if config == 'Sobre costo':
            if self.rentabilidad < 0:
                raise ValidationError("La rentabilidad no puede ser inferior a 0%") 
            if self.cantidad == 0:
                raise ValidationError("La cantidad debe ser superior a 1.") 

        if self.validad_udm() != True:
            raise ValidationError(f"Validar Unidad de medida.") 
        
        return super().clean()

    @property
    def rentabilidadNeta(self):
        costo_unitario = float(self.producto.costo_unitario) or 0
        precio_venta_unitario = float(self.precio()) or 0
        diferencia = float(precio_venta_unitario) - float(costo_unitario)
        if costo_unitario == 0:
            margen = round(0,2)
        else:
            margen = round(float(100) * float(float(diferencia) / float(costo_unitario)),2)
        return margen

    def validad_udm(self):
        '''
            Esta validacion es para ver si las unidades de medida corresponden.
            Solo se usa al guardar un precio de producto
        '''
        unidad_compra=self.producto.unidad_de_medida
        unidad_uso=self.unidad_de_medida
        if unidad_compra==unidad_uso:
            return True
        else: 
            if unidad_compra == 'Unidades':
                raise ValidationError(f"El precio tiene que tener la siguiente unidad de medida: Unidades")
            elif unidad_compra == 'Mt2s':
                raise ValidationError(f"El precio tiene que tener la siguiente unidad de medida: Mt2s")
            elif unidad_compra == 'Kilos':
                if unidad_uso != 'Gramos':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Kilos o Gramos")
            elif unidad_compra == 'Gramos':
                if unidad_uso != 'Kilos':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Kilos o Gramos")
            elif unidad_compra == 'Litros':    
                if unidad_uso != 'Mililitros':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Litros o Mililitros")
            elif unidad_compra == 'Mililitros':
                if unidad_uso != 'Litros':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Litros o Mililitros")
            elif unidad_compra == 'Onzas':    
                if unidad_uso != 'Libras':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Libras o Onzas")
            elif unidad_compra == 'Libras':
                if unidad_uso != 'Onzas':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Libras o Onzas")
            elif unidad_compra == 'Mts':    
                if unidad_uso != 'Cms':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Mts o Cms")
            elif unidad_compra == 'Cms':
                if unidad_uso != 'Mts':
                    raise ValidationError(f"El precio tiene que tener una de las siguientes unidades de medida: Mts o Cms")
            return True

    def costo_unit(self):
        costo= float(self.producto.costo_unitario_calculado())   
        return costo
    
    def precio_unitario_calculado(self):
        config = configuracion.objects.first()
        precio_venta = 0

        if self.producto.tipo == 'Simple':
            costo_unitario = float(self.producto.costo_unitario) or 0
            if self.unidad_de_medida != self.producto.unidad_de_medida:
                if self.unidad_de_medida == "Kilos" or self.unidad_de_medida == "Litros":
                    costo_unitario = float(costo_unitario) * 1000
                elif self.unidad_de_medida == "Gramos" or self.unidad_de_medida == "Mililitros":
                    costo_unitario = float(costo_unitario) / 1000
                elif self.unidad_de_medida == "Mts":
                    costo_unitario = float(costo_unitario) * 100
                elif self.unidad_de_medida == "Cms":
                    costo_unitario = float(costo_unitario) / 100 
                elif self.unidad_de_medida == "Onzas":
                    costo_unitario = float(costo_unitario) / 16
                elif self.unidad_de_medida == "Libras":
                    costo_unitario = float(costo_unitario) * 16    
        else:
            costo_unitario = self.producto.costo_unitario_calculado()

        if config.calculo_rentabilidad == 'Sobre costo':
            
            if config.precio_venta_automatico:
                # Calcular precio unitario basado en la rentabilidad
                precio_venta = float(costo_unitario) * (1 + float(self.rentabilidad) / 100)
            else:
                # Usar el precio manual si no es automático
                precio_venta = float(self.precio_manual) or 0
        else:
            # Lógica de cálculo basada en otro método de rentabilidad

            precio_venta = float(costo_unitario) / (100 - float(self.rentabilidad)) * 100
            
        return float(precio_venta) * float(self.cantidad)

    def precio_unitario_madre(self):
        costo_unitario = float(self.precio_unitario_calculado()) / float(self.cantidad)
        if self.unidad_de_medida != self.producto.unidad_de_medida:
            if self.unidad_de_medida == "Kilos" or self.unidad_de_medida == "Litros":
                costo_unitario = float(costo_unitario) / 1000
            elif self.unidad_de_medida == "Gramos" or self.unidad_de_medida == "Mililitros":
                costo_unitario = float(costo_unitario) * 1000
            elif self.unidad_de_medida == "Mts":
                costo_unitario = float(costo_unitario) / 100
            elif self.unidad_de_medida == "Cms":
                costo_unitario = float(costo_unitario) * 100 
            elif self.unidad_de_medida == "Onzas":
                costo_unitario = float(costo_unitario) * 16
            elif self.unidad_de_medida == "Libras":
                costo_unitario = float(costo_unitario) / 16  

        return round(costo_unitario,2)
    
    def save(self, *args, **kwargs):
        # Calcula el precio unitario y total antes de guardar
        self.precio_unitario = self.precio_unitario_calculado()
        self.precio_total = self.precio_unitario
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'precio'
        verbose_name_plural ='💱 Precios de productos' 


# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
class Merma(models.Model):
    fecha = models.DateField(auto_now=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=15,decimal_places=2,blank=False,null=False,default=0)
    costos_totales = models.DecimalField(max_digits=15,decimal_places=2,blank=False,null=False,default=0)
    motivo = models.CharField(max_length=255,blank=False,null=False)

    def __str__(self):
        return f'{self.producto}'

    class Meta:
        verbose_name = 'merma'
        verbose_name_plural = '⛔ Mermas'

    def clean(self):
        if self.cantidad < 1:
            raise ValidationError("La cantidad debe ser positiva.") 
        super().clean()

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Metodos para acceder a los valores de forma dinamica
#
class MovimientoProducto(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    detalle = models.CharField(max_length=255,blank=True, null=True)
    compra = models.ForeignKey('compras.Compra', on_delete=models.CASCADE, null=True, blank=True)
    pedido = models.ForeignKey('pedidos.Pedido', on_delete=models.CASCADE, null=True, blank=True)
    inventario = models.ForeignKey(Deposito, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False, blank=False)
    entrada = models.DecimalField(max_digits=25, decimal_places=2,default=0 ,blank=False,null=False)
    salida = models.DecimalField(max_digits=25, decimal_places=2,default=0 ,blank=False,null=False) 
    estado = models.BooleanField(default=False)
    
    def clean(self): 
        return super().clean()
    
    def __str__(self):
        return f'Precio {self.detalle}'
    
    class Meta:
        verbose_name = 'movimiento'
        verbose_name_plural ='🔀 Movimientos' 




