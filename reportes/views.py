from django.db.models import Count, Avg, F, ExpressionWrapper, IntegerField
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from cursos.models import Curso
from cursos.permissions import EsAdministrador


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