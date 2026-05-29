from django.contrib import admin
from .models import Inscripcion


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "estudiante",
        "curso",
        "fecha_inscripcion"
    )