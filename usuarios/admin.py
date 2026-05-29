from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Información de rol", {"fields": ("rol",)}),
    )

    list_display = ("id", "username", "email", "rol", "is_active", "is_staff")
    list_filter = ("rol", "is_active", "is_staff")