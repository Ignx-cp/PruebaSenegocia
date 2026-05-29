from django.db.models import Count, Avg, F, ExpressionWrapper, IntegerField
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from inscripciones.models import Inscripcion
from django.core.cache import cache

from cursos.models import Curso
from cursos.permissions import EsAdministrador

Usuario = get_user_model()


@api_view(["GET"])
@permission_classes([EsAdministrador])
def cursos_con_inscritos(request):
    cursos = Curso.objects.annotate(
        cantidad_inscritos=Count("inscripciones")
    ).values(
        "id",
        "nombre",
        "capacidad_maxima",
        "cantidad_inscritos",
        "activo",
    )

    return Response(cursos)


@api_view(["GET"])
@permission_classes([EsAdministrador])
def cupos_disponibles(request):
    cursos = Curso.objects.annotate(
        inscritos=Count("inscripciones")
    ).annotate(
        cupos_disponibles=ExpressionWrapper(
            F("capacidad_maxima") - F("inscritos"),
            output_field=IntegerField()
        )
    ).values(
        "id",
        "nombre",
        "capacidad_maxima",
        "inscritos",
        "cupos_disponibles",
        "activo",
    )

    return Response(cursos)


@api_view(["GET"])
@permission_classes([EsAdministrador])
def promedio_notas_por_curso(request):
    cursos = Curso.objects.annotate(
        promedio_notas=Avg("inscripciones__evaluacion__nota")
    ).values(
        "id",
        "nombre",
        "promedio_notas",
    )

    return Response(cursos)

@api_view(["GET"])
@permission_classes([EsAdministrador])
def cursos_de_estudiante(request, estudiante_id):
    if not Usuario.objects.filter(
        id=estudiante_id,
        rol=Usuario.Roles.ESTUDIANTE
    ).exists():
        return Response(
            {"detail": "Estudiante no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    cursos = Inscripcion.objects.filter(
        estudiante_id=estudiante_id
    ).select_related(
        "curso"
    ).annotate(
        promedio=Avg("evaluacion__nota")
    ).values(
        "curso__id",
        "curso__nombre",
        "promedio"
    )

    return Response(cursos)


@api_view(["GET"])
@permission_classes([EsAdministrador])
def estudiantes_de_curso(request, curso_id):
    if not Curso.objects.filter(id=curso_id).exists():
        return Response(
            {"detail": "Curso no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    estudiantes = Inscripcion.objects.filter(
        curso_id=curso_id
    ).select_related(
        "estudiante"
    ).annotate(
        promedio=Avg("evaluacion__nota")
    ).values(
        "estudiante__id",
        "estudiante__username",
        "promedio"
    )

    return Response(estudiantes)


@api_view(["GET"])
@permission_classes([EsAdministrador])
def top_3_estudiantes(request):
    cache_key = "top_3_estudiantes"
    data = cache.get(cache_key)

    if data is not None:
        return Response(data)

    estudiantes = list(
        Usuario.objects.filter(
            rol=Usuario.Roles.ESTUDIANTE,
            inscripciones__evaluacion__isnull=False
        )
        .annotate(
            promedio_global=Avg("inscripciones__evaluacion__nota")
        )
        .order_by("-promedio_global")
        .values(
            "id",
            "username",
            "promedio_global"
        )[:3]
    )

    cache.set(cache_key, estudiantes, timeout=300)

    return Response(estudiantes)