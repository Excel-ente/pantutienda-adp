from django.shortcuts import render
from configuracion.envio_mails import send_mail_alta_proveedor
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ConfiguracionForm
from .models import configuracion

def send_mail_venta(request):
    proveedor = 'kevincito'  # Nombre del proveedor dinámico
    email = 'turkienich@gmail.com'  # Correo del proveedor
    send_mail_alta_proveedor(proveedor, email)  # Llama a la función con los parámetros correctos
    return HttpResponse("Correo enviado.")


def onboarding(request):
    # Si existe una configuración, redirige a otra vista
    # if configuracion.objects.exists():
    #     return redirect('home')

    if request.method == 'POST':
        form = ConfiguracionForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva configuración
            return redirect('/app/')  # Redirige a la vista principal después de guardar
    else:
        form = ConfiguracionForm()

    context = {
        'form': form,
    }
    return render(request, 'onboarding.html', context)