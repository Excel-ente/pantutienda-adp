# from django.db import models
# from django.utils import timezone
# from inventario.models import Deposito,Producto
# from agenda.models import Vendedor,Chofer,Proveedor
# from configuracion.models import configuracion
# from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User



# # -----------------------------------------------------------------------------
# # Metodos para acceder a los valores de forma dinamica
# #
# class detalleNotaCredito(models.Model):
#     from compra.models import NotaDeCreditoCompra

#     NotaCredito = models.ForeignKey(NotaDeCreditoCompra, on_delete=models.CASCADE,blank=True,null=True)
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE,blank=False,null=False)
#     Cantidad = models.DecimalField(max_digits=25, decimal_places=3,default=1,blank=False,null=False)
#     Precio = models.DecimalField(max_digits=25,decimal_places=3,default=0,blank=False,null=False)

#     class Meta:
#         verbose_name = 'detalle de Nota de credito'
#         verbose_name_plural = 'Detalles de Nota de credito'

#     def clean(self):
#         super().clean()

#         # Verificar que la cantidad no exceda la cantidad disponible en la orden de compra
#         detalles_compra = detalleCompra.objects.filter(Compra=self.NotaCredito.compra, producto=self.producto)
#         if not detalles_compra.exists():
#             raise ValidationError(f'El producto {self.producto.nombre} no está en la orden de compra.')

#         total_compra = sum(detalle.Cantidad for detalle in detalles_compra)
#         total_notas_credito = detalleNotaCredito.objects.filter(NotaCredito__compra=self.NotaCredito.compra, producto=self.producto).exclude(id=self.id).aggregate(Sum('Cantidad'))['Cantidad__sum'] or 0

#         if self.Cantidad > (total_compra - total_notas_credito):
#             raise ValidationError(f'La cantidad de la nota de crédito para el producto {self.producto.nombre} no puede exceder la cantidad disponible en la orden de compra. Disponible: {total_compra - total_notas_credito}')

#         # Verificar que el precio sea igual al precio de compra
#         precio_compra = detalles_compra.first().Precio
#         if self.Precio != precio_compra:
#             raise ValidationError(f'El precio de la nota de crédito para el producto {self.producto.nombre} debe ser igual al precio de compra. Precio de compra: {precio_compra}')


#     def Subtotal(self):
#         subtotal = float(self.Precio) * float(self.Cantidad)
#         return subtotal
    
   







