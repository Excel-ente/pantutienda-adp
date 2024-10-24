from django.shortcuts import render
from configuracion.envio_mails import send_mail_alta_proveedor
from django.http import HttpResponse

def send_mail_venta(request):
    proveedor = 'kevincito'  # Nombre del proveedor dinámico
    email = 'turkienich@gmail.com'  # Correo del proveedor
    send_mail_alta_proveedor(proveedor, email)  # Llama a la función con los parámetros correctos
    return HttpResponse("Correo enviado.")
