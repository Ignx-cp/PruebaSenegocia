from django.urls import path

from .views import (
    cursos_con_inscritos,
    cupos_disponibles,
    promedio_notas_por_curso,
    cursos_de_estudiante,
    estudiantes_de_curso,
    top_3_estudiantes,
)

urlpatterns = [
    path("reportes/cursos-inscritos/", cursos_con_inscritos),
    path("reportes/cupos-disponibles/", cupos_disponibles),
    path("reportes/promedio-notas/", promedio_notas_por_curso),

    path(
        "reportes/estudiantes/<int:estudiante_id>/cursos/",
        cursos_de_estudiante,
    ),
    path(
        "reportes/cursos/<int:curso_id>/estudiantes/",
        estudiantes_de_curso,
    ),
    path(
        "reportes/top-estudiantes/",
        top_3_estudiantes,
    ),
]