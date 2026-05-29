from rest_framework import serializers

from .models import Curso


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = [
            "id",
            "nombre",
            "descripcion",
            "capacidad_maxima",
            "activo",
            "fecha_creacion",
        ]
        read_only_fields = ["id", "fecha_creacion"]