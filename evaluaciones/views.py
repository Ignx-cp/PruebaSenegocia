from rest_framework.viewsets import ModelViewSet
from .models import Evaluacion
from .serializers import EvaluacionSerializer
from cursos.permissions import EsAdministrador


class EvaluacionViewSet(ModelViewSet):
    queryset = Evaluacion.objects.select_related(
    "inscripcion",
    "inscripcion__estudiante",
    "inscripcion__curso",
    ).order_by("-fecha")
    serializer_class = EvaluacionSerializer
    permission_classes = [EsAdministrador]