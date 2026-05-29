from django.urls import path
from .views import (
    cursos_con_inscritos,
    cupos_disponibles,
    promedio_notas_por_curso,
)

urlpatterns = [
    path("reportes/cursos-inscritos/", cursos_con_inscritos),
    path("reportes/cupos-disponibles/", cupos_disponibles),
    path("reportes/promedio-notas/", promedio_notas_por_curso),
]