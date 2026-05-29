from django.contrib import admin
from .models import Evaluacion


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "inscripcion",
        "nota",
        "fecha"
    )