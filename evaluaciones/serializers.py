from rest_framework import serializers
from .models import Evaluacion


class EvaluacionSerializer(serializers.ModelSerializer):
    estudiante = serializers.CharField(
        source="inscripcion.estudiante.username",
        read_only=True
    )
    curso = serializers.CharField(
        source="inscripcion.curso.nombre",
        read_only=True
    )

    class Meta:
        model = Evaluacion
        fields = [
            "id",
            "inscripcion",
            "estudiante",
            "curso",
            "nota",
            "fecha",
            "observacion",
        ]
        read_only_fields = [
            "fecha",
            "estudiante",
            "curso",
        ]

    def validate_nota(self, value):
        if value < 1 or value > 7:
            raise serializers.ValidationError(
                "La nota debe estar entre 1.0 y 7.0"
            )
        return value