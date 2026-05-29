from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Curso
from .serializers import CursoSerializer
from .permissions import EsAdministrador


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.filter(activo=True).order_by("id")
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticated, EsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["activo"]
    search_fields = ["nombre"]

    def perform_destroy(self, instance):
        instance.activo = False
        instance.save()