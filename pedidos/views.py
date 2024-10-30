from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from pedidos.utils import generar_movimiento_venta
from .models import Pedido, ItemPedido
from agenda.models import Cliente
from configuracion.models import configuracion
from inventario.models import Producto,ProductoPrecio
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages


# proceso de pedido ----------------------------------------------------------------------

@login_required(login_url='/admin/login/')
def confirmar_pedido(request, id):

    pedido = get_object_or_404(Pedido, id=id)
    config = configuracion.objects.first()

    if not config.gestionar_entrega:
        if not config.gestionar_armar_pedido:
            pedido.estado = 'completado'
            pedido.save()
            messages.success(request, f'Pedido completado!')
            
        else:
            pedido.estado = 'en_preparacion'
            pedido.save()
            messages.success(request, f'Pedido en preparación!')
      
    else:
        if not config.gestionar_armar_pedido:
            pedido.estado = 'listo'
            pedido.save()
            messages.success(request, f'Pedido completado!')
         
        else:
            pedido.estado = 'en_preparacion'
            pedido.save()
            messages.success(request, f'Pedido en preparación!')
           
    generar_movimiento_venta(pedido)
    return redirect('admin:pedidos_pedido_changelist')

@login_required(login_url='/admin/login/')
def confirmar_armado_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = 'listo'
    pedido.save()
    messages.success(request, f'El pedido ha sido armado correctamente.')

    return redirect('admin:pedidos_pedido_changelist')

@login_required(login_url='/admin/login/')
def iniciar_armado_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = 'en_camino'
    pedido.save()
    messages.success(request, f'El pedido ha sido armado correctamente.')

    return redirect('admin:pedidos_pedido_changelist')

@login_required(login_url='/admin/login/')
def finalizar_entrega_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.estado = 'completado'
    pedido.save()
    messages.success(request, f'El pedido ha sido entregado correctamente.')

    return redirect('admin:pedidos_pedido_changelist')

# -----------------------------------------------------------------------------------------
# vistas del carrito ----------------------------------------------------------------------

@login_required
def carrito(request):

    try:
        # Intentar obtener el cliente asociado al usuario
        cliente = Cliente.objects.get(usuario=request.user)

        if cliente.habilitado == False:
            return render(request, 'cuenta_suspendida.html')
        
    except Cliente.DoesNotExist:
        # Si no existe, redirigir a la vista de "cuenta no verificada"
        return render(request, 'cuenta_no_verificada.html')



    if request.method == 'GET':
        # Crear un pedido pendiente si no existe uno
        pedido, creado = Pedido.objects.get_or_create(cliente=cliente, estado='abierto')
        items = pedido.items.all()  # Obtener los ítems del pedido
        total = sum(item.subtotal() for item in items)  # Calcular total

        context = {
            'items': items,
            'total': total,
        }
        return render(request, 'carrito.html', context)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        try:
            # Eliminar el ítem si pertenece al cliente actual
            item = get_object_or_404(ItemPedido, id=item_id, pedido__cliente=cliente)
            item.delete()
            messages.success(request, 'Producto eliminado del carrito.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')

        return redirect('productos')

@login_required
@require_POST
def agregar_al_carrito(request):

    pedidos_pendientes_limite = configuracion.objects.first().limite_pedidos_pendientes

    try:
        # Verificar si el usuario tiene un cliente asociado
        cliente = Cliente.objects.get(usuario=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, "Tu cuenta no está verificada como cliente.")
        return redirect('productos')  # Redirigir con un mensaje de error


    pedidos_pendientes = Pedido.objects.filter(cliente=cliente, estado='abierto').count()

    if pedidos_pendientes >= pedidos_pendientes_limite:
        messages.error(request, f"Tienes {pedidos_pendientes} pedidos en proceso. Una vez confirmado podrás seguir creando nuevos pedidos.")
        return redirect('productos')  # Redirigir con un mensaje de error


    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, estado='abierto')

    producto_id = request.POST['id']
 
    product_precio = request.POST['product_precio_id']  # Usamos el ID directamente

    product_precio_id = ProductoPrecio.objects.get(producto__id=producto_id,id=product_precio).pk

    cantidad = int(request.POST['quantity'])


    # Verificar si el producto y el precio existen
    producto = get_object_or_404(Producto, id=producto_id)
    producto_precio = get_object_or_404(ProductoPrecio, id=product_precio_id)

    # Verificar si el producto ya está en el carrito
    item_existente = ItemPedido.objects.filter(
        pedido=pedido, producto=producto, producto_precio=producto_precio
    ).exists()


    if item_existente:
        # Usar mensajes de Django para mostrar alertas en el frontend
        messages.error(request, 'El producto ya está en el carrito.')
        return redirect('productos')  # Redirecciona a la vista de productos


    # Evitar duplicados en el carrito
    item, creado = ItemPedido.objects.get_or_create(
        pedido=pedido,
        producto=producto,
        producto_precio=producto_precio,
        defaults={'cantidad': cantidad, 'precio_unitario': producto_precio.precio_unitario_calculado()}
    )

    if not creado:
        return JsonResponse({'status': 'error', 'message': 'El producto ya está en el carrito'}, status=400)

    return redirect('productos')

@login_required
@require_POST
def actualizar_carrito(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cantidad = int(request.POST.get('quantity'))

        item = get_object_or_404(ItemPedido, id=item_id, pedido__cliente__usuario=request.user)
        item.cantidad = cantidad
        item.save()

        messages.success(request, 'Cantidad actualizada correctamente.')
        
    return redirect('carrito')

@login_required
@require_POST
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemPedido, id=item_id)
    pedido = item.pedido
    # Eliminar el ítem
    item.delete()
    # Si no hay más ítems en el pedido, eliminar el pedido
    if not pedido.items.exists():
        pedido.delete()
    return redirect('carrito')

# ------------------------------------------------------------------------------------------