from inventario.models import MovimientoProducto,Producto
from configuracion.models import configuracion
from pedidos.models import Pedido,ItemPedido


# ---- FUNCION DE CONFIRMACION DE COMPRA -------
 
def generar_movimiento_venta(pedido):
    """
    Genera movimientos de inventario para una compra confirmada.
    """

    # Obtener los detalles de la compra
    detalles = ItemPedido.objects.filter(pedido=pedido)

    # Recorrer cada detalle de la compra para generar el movimiento
    for detalle in detalles:
        MovimientoProducto.objects.create(
            detalle=f'Movimientos generados para la venta {pedido.id}',
            inventario=detalle.pedido.deposito,  # Depósito donde se ingresarán los productos
            pedido=detalle.pedido, # Compra asociada
            producto=detalle.producto_precio.producto,  # Producto que se está moviendo
            entrada=0,  # Cantidad que ingresa al inventario
            salida=detalle.cantidad_madre(),  # No hay salida porque es una compra (solo entrada)
            estado=False  # Marcamos el movimiento como confirmado
        )
        
    return f'Movimientos generados para la venta {pedido.id}'


# --------------------