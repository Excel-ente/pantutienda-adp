from django.contrib import admin
from .models import FailedLoginAttempt

@admin.register(FailedLoginAttempt)
class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('ip_address','attempt_time')
    readonly_fields = ('ip_address','attempt_time','ciudad','region','pais','organizacion')    
