# ------------------------------------------------------------------------------------------
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from front.models import Landing
from inventario.models import Producto,ProductoPrecio
from pedidos.models import Pedido
from agenda.models import Cliente,Proveedor,Chofer,Vendedor,DireccionEntregaCliente
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
from configuracion.models import configuracion
from django.utils.safestring import mark_safe
import json
# ------------------------------------------------------------------------------------------
# Funciones
def obtener_perfil(user):

    '''
        Esta funcion, consulta el perfil del usuario en caché, si no existe, lo crea.

        El caché dura: 3600 seg ( 1 Hora )
    '''

    cache_key = f"perfil_{user.pk}" 
    perfil = cache.get(cache_key)

    if not perfil:
        cliente = Cliente.objects.filter(usuario=user).first()
        proveedor = Proveedor.objects.filter(usuario=user).first()
        chofer = Chofer.objects.filter(usuario=user).first()
        vendedor = Vendedor.objects.filter(usuario=user).first()

        if cliente:
            cliente_habilitado = cliente.habilitado
            tipo_cliente = "cliente"
            numero_usuario = cliente.pk
            empresa = ""
        elif proveedor:
            tipo_cliente = "proveedor"
            numero_usuario = proveedor.pk
            empresa = proveedor.empresa
        elif chofer:
            tipo_cliente = "chofer"
            numero_usuario = chofer.pk
            empresa = ""
        elif vendedor:
            tipo_cliente = "vendedor"
            numero_usuario = vendedor.pk
            empresa = ""
        else:
            tipo_cliente = "sin rol asignado"
            numero_usuario = "sin rol asignado"
            empresa = ""

        perfil = {
            'tipo_cliente': tipo_cliente,
            'numero_usuario': numero_usuario,
            'empresa': empresa,
        }

        cache.set(cache_key, perfil, timeout=3600)

    return perfil

# ------------------------------------------------------------------------------------------
# Vista de loging
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        
        if not request.user.check_password(current_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('home')

        if new_password != confirm_new_password:
            messages.error(request, 'Las nuevas contraseñas no coinciden.')
            return redirect('home')

        # Cambiar la contraseña
        request.user.set_password(new_password)
        request.user.save()

        # Actualizar la sesión para evitar cierre de sesión después del cambio
        update_session_auth_hash(request, request.user)

        messages.success(request, '¡La contraseña ha sido cambiada exitosamente!')
        return redirect('home')

    return redirect('home')

def custom_logout(request):
    logout(request)
    return redirect('/')

@login_required
def cuenta_no_verificada(request):
    # Verifica si el usuario tiene un cliente asociado
    usuario = request.user
    perfil = obtener_perfil(usuario)

    # Contexto que se pasará al template
    context = {
        'usuario': usuario.username,
        'tipo_cliente': perfil['tipo_cliente'],
        'numero_usuario': perfil['numero_usuario'],
        'empresa': perfil['empresa'],
    }
    
    return render(request, 'cuenta_no_verificada.html',context)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# Vistas App


def home(request):
    landing = Landing.objects.first()  # Asegúrate de que haya una landing en la base de datos

    if not landing:
        return render(request, '404.html')  # Si no hay un objeto landing, renderiza una página de error o similar.

    # Obtén las secciones activas y ordenadas
    secciones = landing.section_set.filter(is_active=True).order_by('order')


    # Si el usuario está autenticado, obtenemos su perfil
    if request.user.is_authenticated:
        perfil = obtener_perfil(request.user)
        context = {
            'landing': landing,
            'secciones': secciones,
            'usuario': request.user.username,
            'tipo_cliente': perfil['tipo_cliente'],
            'numero_usuario': perfil['numero_usuario'],
            'empresa': perfil['empresa'],
            'link_contacto': '+541157045506',
            'mensaje': f'Hola, soy {request.user}, me contacto por ...',
        }
    else:
        context = {
            'landing': landing,
            'secciones': secciones,
            'usuario': 'Anónimo',
            'numero_usuario': None,
            'tipo_cliente': 'Visitante',
            'link_contacto': '+541157045506',
            'mensaje': 'Hola, soy un visitante, me contacto por...',
        }

    return render(request, 'landing/index.html', context)




# ------------------------------------------------------------------------------------------

def carrito(request):
    usuario = request.user

    if usuario.is_authenticated:
        perfil = obtener_perfil(usuario)

        context = {
            'usuario': usuario.username,
            'tipo_cliente': perfil['tipo_cliente'],
            'numero_usuario': perfil['numero_usuario'],
            'empresa': perfil['empresa'],
        }
    else:
        # Si el usuario no está autenticado, redirigir al login
        return redirect('login')

    return render(request, 'carrito.html', context)

# ------------------------------------------------------------------------------------------


@login_required
def productos(request):
    # Verifica si el usuario tiene un cliente asociado
    es_cliente = Cliente.objects.filter(usuario=request.user).exists()
    if not es_cliente:
        return redirect('cuenta_no_verificada')

    cliente = Cliente.objects.get(usuario=request.user)
    cliente_habilitado = cliente.habilitado

    if not cliente.lista_de_precio:
        # Si el cliente no tiene una lista de precios asignada, no verá productos
        context = {
            'cliente_habilitado': cliente_habilitado,
            'es_cliente': True,
            'productos_precio': [],
            'sin_lista_de_precio': True,
        }
        return render(request, 'productos.html', context)

    lista_de_precio = cliente.lista_de_precio

    # Obtenemos los ProductoPrecio asociados a la lista de precios del cliente
    productos_precio = ProductoPrecio.objects.filter(
        lista=lista_de_precio,
        producto__habilitar_venta=True
    ).select_related('producto')

    # Preparamos los datos para pasarlos al template
    productos_precio_list = []
    for pp in productos_precio:
        productos_precio_list.append({
            'id': pp.id,
            'producto_id': pp.producto.id,
            'producto_nombre': pp.producto.nombre,
            'producto_imagen': pp.producto.imagen.url if pp.producto.imagen else '',
            'precio_unitario': float(pp.precio_unitario_calculado()),
            'presentacion': str(pp),  # Convertimos a cadena
            'cantidad': pp.cantidad,
            'unidad_de_medida': str(pp.unidad_de_medida),  # Convertimos a cadena
        })

    # Serializamos los datos a JSON y los marcamos como seguros
    productos_precio_json = mark_safe(json.dumps(productos_precio_list))

    context = {
        'cliente_habilitado': cliente_habilitado,
        'es_cliente': es_cliente,
        'productos_precio_json': productos_precio_json,
    }
    return render(request, 'productos.html', context)



# ------------------------------------------------------------------------------------------
@login_required
def pedidos_view(request):
    '''
        Esta vista retorna los pedidos del cliente (usuario) activo.
    '''

    usuario = request.user
    pedidos_data = []

    cliente = Cliente.objects.filter(usuario=usuario).first()
    if not cliente:
        return JsonResponse({'pedidos': pedidos_data})

    # Obtener los pedidos del cliente excluyendo los pendientes
    pedidos = Pedido.objects.exclude(estado="abierto").filter(cliente=cliente).prefetch_related('items__producto')

    # Convertimos los pedidos a un formato JSON
    for pedido in pedidos:
        pedidos_data.append({
            'id': pedido.id,
            'total': pedido.total(),
            'estado': pedido.estado,
            'items': [
                {
                    'producto': item.producto.nombre,
                    'cantidad': item.cantidad,
                    'subtotal': item.subtotal()
                }
                for item in pedido.items.all()
            ]
        })
        
    return JsonResponse({'pedidos': pedidos_data})


# ------------------------------------------------------------------------------------------


import json  # Asegúrate de importar el módulo json

@login_required
def confirmar_pedido(request):


    cliente = Cliente.objects.filter(usuario=request.user).first()

    if not cliente:
        return JsonResponse({'error': 'No tienes una cuenta de cliente asociada.'}, status=400)

    pedido = Pedido.objects.filter(cliente=cliente, estado='abierto').first()
  

    if not pedido:
        return JsonResponse({'error': 'No tienes un pedido abierto.'}, status=404)

    if request.method == "GET":
   
        items = [
            {
                'producto': item.producto.nombre,
                'cantidad': item.cantidad,
                'subtotal': float(item.subtotal())
            }
            for item in pedido.items.all()
        ]
        total = float(pedido.total())

        # Obtener todas las direcciones del cliente
        direcciones = DireccionEntregaCliente.objects.filter(Cliente=cliente)
        direcciones_list = [
            {'id': direccion.id, 'direccion': direccion.direccion}
            for direccion in direcciones
        ]

        return JsonResponse({'items': items, 'total': total, 'direcciones': direcciones_list})

    if request.method == "POST":
        
        data = json.loads(request.body)
   
        direccion_id = data.get('direccion_id')
    
        if not direccion_id:
            return JsonResponse({'error': 'No se proporcionó una dirección.'}, status=400)

        try:
            direccion = DireccionEntregaCliente.objects.get(id=direccion_id, Cliente=cliente)
        except DireccionEntregaCliente.DoesNotExist:
            return JsonResponse({'error': 'La dirección seleccionada no es válida.'}, status=400)


        pedido.estado = 'pendiente'
        pedido.direccion_entrega_cliente = direccion
        pedido.save()

        return JsonResponse({'success': True})


# ------------------------------------------------------------------------------------------
def custom_login(request):
    
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '¡Bienvenido!')
            return redirect('home')  # Redirigir al home
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')  # Redirigir de nuevo a login en caso de error

    return render(request, 'login.html')
    
def registro(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
            return redirect('registro')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Registro exitoso. Bienvenido!')
        return redirect('/')

    return render(request, 'registro.html')
# ------------------------------------------------------------------------------------------

