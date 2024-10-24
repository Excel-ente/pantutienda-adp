from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
import openpyxl
import json
from .utils import *

def descargar_excel(request, id_compra):
    compra = Compra.objects.get(id=id_compra)
    detalles = detalleCompra.objects.filter(compra=compra)

    # Crear archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f'Compra {compra.id}'

    # Agregar encabezados
    ws.append(['Producto', 'Precio Anterior', 'Precio Actual', 'Diferencia (%)'])

    # Agregar datos
    for detalle in detalles:
        diferencia = detalle.resultado_compra()
        ws.append([
            detalle.producto.nombre,
            detalle.producto.costo_unitario,
            detalle.precio_calculado,
            diferencia,
        ])

    # Preparar la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="Compra_{compra.id}.xlsx"'
    wb.save(response)
    return response

@login_required(login_url='/admin/login/')
def popup_comparar_productos(request, id_compra):
    compra = get_object_or_404(Compra, id=id_compra)
    detalles = detalleCompra.objects.filter(compra=compra)

    productos_data = [
        {
            'producto': detalle.producto.nombre,
            'costo_anterior': float(detalle.producto.costo_unitario),
            'precio_actual': float(detalle.precio_calculado),
            'diferencia': float(detalle.resultado_compra()),
        }
        for detalle in detalles
    ]

    context = {
        'compra': compra,
        'productos_json': json.dumps(productos_data),
    }
    return render(request, 'popup_comparar_productos.html', context)

@login_required(login_url='/admin/login/')
def ver_google_maps(request, id_flete):
    compra = get_object_or_404(Compra, id=id_flete)
    flete = FleteCompra.objects.filter(compra=compra).first()
    maps_url = flete.ruta_maps
    return redirect(maps_url)


@login_required(login_url='/admin/login/')
def confirmar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    config = configuracion.objects.first()

    try:

        if config.confirmar_viaje_compra:
            compra.en_transito = True
       
        # Intentar generar los movimientos de inventario
        generar_movimiento_compra(compra)

        # Confirmar la compra
        compra.estado = True
        compra.save()

        # Mensaje de éxito si todo sale bien
        messages.success(request, f'La compra fue confirmada correctamente.')
    
    except Exception as e:
        # Si ocurre algún error, se muestra un mensaje de error al usuario
        messages.error(request, f'Error al confirmar la compra: {str(e)}')

    return redirect('admin:compras_compra_changelist')


@login_required(login_url='/admin/login/')
def iniciar_descarga(request, id):
    compra = get_object_or_404(Compra, id=id)
    compra.en_descarga = True
    compra.en_transito = False
    compra.save()
    messages.success(request, f'La descarga se inició correctamente.')

    return redirect('admin:compras_compra_changelist')

@login_required(login_url='/admin/login/')
def terminar_descarga(request, id):
    compra = get_object_or_404(Compra, id=id)


    try:
        compra.en_descarga = False
        compra.descargas += 1
        generar_movimiento_compra(compra)
        compra.save()
        messages.success(request, f'La descarga se finalizó correctamente!')

        return redirect('admin:compras_compra_changelist')
    
    except Exception as e:
        # Si ocurre algún error, se muestra un mensaje de error al usuario
        messages.error(request, f'Error al finalizar la compra: {str(e)}')

    return redirect('admin:compras_compra_changelist')
