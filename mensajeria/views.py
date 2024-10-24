from django.shortcuts import redirect
from django.http import JsonResponse
from .models import Mensaje
from django.contrib.auth.decorators import login_required

@login_required
def enviar_mensaje(request):
    titulo = request.POST.get('titulo')
    cuerpo = request.POST.get('cuerpo')

    if titulo and cuerpo:
        mensaje = Mensaje.objects.create(
            usuario=request.user,
            titulo=titulo,
            cuerpo=cuerpo,
            estado='pendiente'
        )
        return JsonResponse({'success': True, 'message': 'Mensaje enviado con éxito'})
    return JsonResponse({'success': False, 'message': 'Error al enviar el mensaje'})
