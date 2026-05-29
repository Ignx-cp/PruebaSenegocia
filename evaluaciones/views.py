from django.core.cache import cache
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

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("top_3_estudiantes")

    def perform_update(self, serializer):
        serializer.save()
        cache.delete("top_3_estudiantes")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete("top_3_estudiantes")