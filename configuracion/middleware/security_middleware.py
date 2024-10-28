import time
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden

class BruteForceProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configuración de intentos y duración de bloqueo desde settings
        self.lockout_threshold = getattr(settings, 'AUTHENTICATION_LOCKOUT_THRESHOLD', 5)
        self.lockout_duration = getattr(settings, 'AUTHENTICATION_LOCKOUT_DURATION', 300)  # en segundos

    def __call__(self, request):
        # Solo monitorear intentos fallidos en la vista de inicio de sesión
        if request.path == '/login/' and request.method == 'POST':
            # Obtener la IP del usuario
            user_ip = request.META.get('REMOTE_ADDR')
            cache_key_attempts = f"failed_login_attempts_{user_ip}"
            cache_key_lockout = f"lockout_{user_ip}"

            # Verificar si la IP está bloqueada
            if cache.get(cache_key_lockout):
                return HttpResponseForbidden("Demasiados intentos fallidos. Intente nuevamente más tarde.")

            # Intentos fallidos actuales
            failed_attempts = cache.get(cache_key_attempts, 0)

            # Comprobar credenciales incorrectas y aumentar contador
            username = request.POST.get('username')
            password = request.POST.get('password')
            from django.contrib.auth import authenticate
            user = authenticate(request, username=username, password=password)

            if user is None:  # Incrementar contador en fallo
                failed_attempts += 1
                cache.set(cache_key_attempts, failed_attempts, timeout=self.lockout_duration)

                # Bloquear IP si el límite de intentos es alcanzado
                if failed_attempts >= self.lockout_threshold:
                    cache.set(cache_key_lockout, True, timeout=self.lockout_duration)
                    return HttpResponseForbidden("Demasiados intentos fallidos. La IP ha sido bloqueada temporalmente.")

            else:  # Restablecer contador en inicio exitoso
                cache.delete(cache_key_attempts)

        # Continuar con la respuesta normal si no hay bloqueo
        return self.get_response(request)
