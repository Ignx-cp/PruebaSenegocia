from rest_framework import serializers

from .models import Inscripcion


class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = [
            "id",
            "estudiante",
            "curso",
            "fecha_inscripcion",
        ]
        read_only_fields = [
            "id",
            "fecha_inscripcion",
        ]
        validators = []