from inventario.models import MovimientoProducto,Producto
from configuracion.models import configuracion
from compras.models import detalleCompra,Compra


# ---- FUNCION DE CONFIRMACION DE COMPRA -------
 
def generar_movimiento_compra(compra):
    """
    Genera movimientos de inventario para una compra confirmada.
    """
    actualizar_autom = configuracion.objects.first().confirmar_pisar_costo

    # Obtener los detalles de la compra
    detalles = detalleCompra.objects.filter(compra=compra)

    # Recorrer cada detalle de la compra para generar el movimiento
    for detalle in detalles:
        MovimientoProducto.objects.create(
            detalle=f'Movimiento generado por la confirmación de la compra {compra.id}',
            inventario=compra.deposito,  # Depósito donde se ingresarán los productos
            compra=detalle.compra, # Compra asociada
            producto=detalle.producto,  # Producto que se está moviendo
            entrada=detalle.cantidad,  # Cantidad que ingresa al inventario
            salida=0,  # No hay salida porque es una compra (solo entrada)
            estado=False  # Marcamos el movimiento como confirmado
        )

        if (actualizar_autom == False) or (actualizar_autom == True and detalle.ActualizarCosto):
            # Actualizar costo
            item=Producto.objects.get(id=detalle.producto.pk)
            item.costo_unitario = detalle.precio_calculado
            item.save()




    return f'Movimientos generados para la compra {compra.id}'


# --------------------



def confirmar_movimiento_compra(compra):
    """
    comfirma movimientos de inventario para una compra confirmada.
    """
    # Obtener los detalles de la compra
    compra = Compra.objects.get(id=compra.pk)
    compra.estado = True
    compra.save()

    return f'Confirmado!'




