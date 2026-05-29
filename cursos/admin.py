from django.contrib import admin
from .models import Curso


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "capacidad_maxima",
        "activo"
    )

    list_filter = (
        "activo",
    )

    search_fields = (
        "nombre",
    )