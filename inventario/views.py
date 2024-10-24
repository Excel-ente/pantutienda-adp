from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto
from django.utils import timezone
# ----------------------------------------------------------------------------------------------------------------
#
#       METOS PARA AUTORIZACION Y DESAUTORIZACION DE PROVEEDORES
#

@login_required
def habilitar_producto(request, id):
    obj = get_object_or_404(Producto, id=id)  # Cambio de nombre de variable
    if not obj.habilitar_venta:

        #Validacion que tenga 1 precio, y que no falten cosas

        if obj.es_publicable():
            obj.habilitar_venta = True
            obj.fecha_habilitacion = timezone.now()
            obj.save()
            messages.success(request, 'El Producto ha sido habilitado exitosamente.')
        else:
            messages.warning(request, 'El Producto no puede ser publicado. Debe contener al menos 1 precio de venta.')

    return redirect('admin:inventario_producto_changelist')

@login_required
def pausar_producto(request, id):
    obj = get_object_or_404(Producto, id=id)  # Cambio de nombre de variable
    if obj.habilitar_venta:
        obj.habilitar_venta = False
        obj.save()
        messages.success(request, 'El Producto ha sido deshabilitado exitosamente.')
    return redirect('admin:inventario_producto_changelist')

#
#
# ----------------------------------------------------------------------------------------------------------------
