from django.conf import settings
from django.db import models

from cursos.models import Curso


class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="inscripciones"
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["estudiante", "curso"],
                name="unique_estudiante_curso"
            )
        ]

    def __str__(self):
        return f"{self.estudiante} - {self.curso}"