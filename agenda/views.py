from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Proveedor,Cliente,Vendedor,Chofer,OnboardingProveedor
from django.utils import timezone
from .utils import *
from configuracion.envio_mails import send_mail_alta_proveedor,send_mail_alta_cliente
from configuracion.models import configuracion
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# ----------------------------------------------------------------------------------------------------------------
#
#       METOS PARA AUTORIZACION Y DESAUTORIZACION DE PROVEEDORES
#

@login_required
def habilitar_proveedor(request, id):
    proveedor_obj = get_object_or_404(Proveedor, id=id)  # Cambio de nombre de variable
    if not proveedor_obj.habilitado:
        try:
            crear_cuenta_comercial_proveedor(proveedor=proveedor_obj)   
        except Exception as e:
            messages.error(request, f'La cuenta comercial no se pudo crear. Detalles del error: {str(e)}')

        try:
            send_mail_alta_proveedor(proveedor=proveedor_obj.usuario.username, email=proveedor_obj.usuario.email)
        except Exception as e:
            messages.error(request, f'La el mail no pudo enviarse. Detalles del error: {str(e)}')

            return redirect('admin:agenda_proveedor_changelist')
        
        proveedor_obj.habilitado = True
        proveedor_obj.fecha_habilitacion = timezone.now()
        proveedor_obj.save()

        messages.success(request, 'El proveedor ha sido habilitado exitosamente.')
    return redirect('admin:agenda_proveedor_changelist')

@login_required
def deshabilitar_proveedor(request, id):
    proveedor_obj = get_object_or_404(Proveedor, id=id)  # Cambio de nombre de variable
    if proveedor_obj.habilitado:
        proveedor_obj.habilitado = False
        proveedor_obj.save()
        messages.success(request, 'El proveedor ha sido deshabilitado exitosamente.')
    return redirect('admin:agenda_proveedor_changelist')

#
#
# ----------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------
#
#       METOS PARA AUTORIZACION Y DESAUTORIZACION DE CLIENTES
#

@login_required
def habilitar_cliente(request, id):

    # Validacion para deshabilitar el envio del mail de bienvenida
    mail_bienvenida = configuracion.objects.first().mail_bienvenida_cliente

    cliente_obj = get_object_or_404(Cliente, id=id) 

    if not cliente_obj.habilitado:
        try:
            crear_cuenta_comercial_cliente(cliente=cliente_obj)   
            messages.info(request,'Cliente habilitado correctamente.')
        except Exception as e:
            messages.error(request, f'La cuenta comercial no se pudo crear. Detalles del error: {str(e)}')

        if mail_bienvenida:
            try:
                send_mail_alta_cliente(cliente=cliente_obj.usuario.username, email=cliente_obj.usuario.email)
                messages.info(request,'Email de bienvenida enviado correctamente.')
            except Exception as e:
                messages.error(request, f'La el mail no pudo enviarse. Detalles del error: {str(e)}')
                return redirect('admin:agenda_cliente_changelist')
            

        cliente_obj.habilitado = True
        cliente_obj.fecha_habilitacion = timezone.now()
        cliente_obj.save()

        messages.success(request, 'El cliente ha sido habilitado exitosamente.')
    return redirect('admin:agenda_cliente_changelist')

@login_required
def deshabilitar_cliente(request, id):
    cliente_obj = get_object_or_404(Cliente, id=id)  # Cambio de nombre de variable
    if cliente_obj.habilitado:
        cliente_obj.habilitado = False
        cliente_obj.save()
        messages.success(request, 'El cliente ha sido deshabilitado exitosamente.')
    return redirect('admin:agenda_cliente_changelist')


#
#
# ----------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------
#
#       METOS PARA AUTORIZACION Y DESAUTORIZACION DE VENDEDOR
#

@login_required
def habilitar_vendedor(request, id):

    vendedor_obj = get_object_or_404(Vendedor, id=id) 

    if not vendedor_obj.habilitado:
        try:
            crear_cuenta_comercial_vendedor(vendedor=vendedor_obj)   
        except Exception as e:
            messages.error(request, f'La cuenta comercial no se pudo crear. Detalles del error: {str(e)}')

        vendedor_obj.habilitado = True
        vendedor_obj.save()

        messages.success(request, 'El vendedor ha sido habilitado exitosamente.')

    return redirect('admin:agenda_vendedor_changelist')

@login_required
def deshabilitar_vendedor(request, id):
    vendedor_obj = get_object_or_404(Vendedor, id=id)  # Cambio de nombre de variable
    if vendedor_obj.habilitado:
        vendedor_obj.habilitado = False
        vendedor_obj.save()
        messages.success(request, 'El vendedor ha sido deshabilitado exitosamente.')
    return redirect('admin:agenda_vendedor_changelist')

#
#
# ----------------------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------------------
#
#       METOS PARA AUTORIZACION Y DESAUTORIZACION DE CHOFER
#

@login_required
def habilitar_chofer(request, id):

    chofer_obj = get_object_or_404(Chofer, id=id) 

    if not chofer_obj.habilitado:
        try:
            crear_cuenta_comercial_chofer(chofer=chofer_obj)   
        except Exception as e:
            messages.error(request, f'La cuenta comercial no se pudo crear. Detalles del error: {str(e)}')

        chofer_obj.habilitado = True
        chofer_obj.save()

        messages.success(request, 'El chofer ha sido habilitado exitosamente.')

    return redirect('admin:agenda_chofer_changelist')

@login_required
def deshabilitar_chofer(request, id):
    chofer_obj = get_object_or_404(Chofer, id=id)  # Cambio de nombre de variable
    if chofer_obj.habilitado:
        chofer_obj.habilitado = False
        chofer_obj.save()
        messages.success(request, 'El chofer ha sido deshabilitado exitosamente.')
    return redirect('admin:agenda_chofer_changelist')





