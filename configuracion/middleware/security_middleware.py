import time
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden
from django.core.cache import cache

class BruteForceProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.lockout_threshold = getattr(settings, 'AUTHENTICATION_LOCKOUT_THRESHOLD', 8)
        self.lockout_duration = getattr(settings, 'AUTHENTICATION_LOCKOUT_DURATION', 60)  # en segundos

    def __call__(self, request):
        # Solo monitorear la ruta de inicio de sesión
        if request.path == '/login/' and request.method == 'POST':
            # Obtener la IP del usuario
            user_ip = request.META.get('REMOTE_ADDR')
            cache_key = f"failed_login_attempts_{user_ip}"

            # Intentos fallidos actuales
            failed_attempts = cache.get(cache_key, 0)

            # Verificar si la IP está bloqueada
            if failed_attempts >= self.lockout_threshold:
                return HttpResponseForbidden("Demasiados intentos fallidos. Intente nuevamente más tarde.")

            # Intento de autenticación
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is None:
                # Incrementar y almacenar el contador de intentos fallidos
                failed_attempts += 1
                cache.set(cache_key, failed_attempts, timeout=self.lockout_duration)
            else:
                # Restablecer intentos fallidos al inicio de sesión exitoso
                cache.delete(cache_key)

        return self.get_response(request)
