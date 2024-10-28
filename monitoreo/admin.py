from django.contrib import admin
from .models import FailedLoginAttempt

@admin.register(FailedLoginAttempt)
class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('ip_address','attempt_time')