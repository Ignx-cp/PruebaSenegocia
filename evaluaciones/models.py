from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from inscripciones.models import Inscripcion


class Evaluacion(models.Model):
    inscripcion = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name="evaluaciones"
    )
    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    fecha = models.DateField()
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.inscripcion} - {self.nota}"