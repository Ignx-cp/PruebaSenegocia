from django.db import models
from inscripciones.models import Inscripcion


class Evaluacion(models.Model):
    inscripcion = models.OneToOneField(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name="evaluacion"
    )
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    fecha = models.DateField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.inscripcion.estudiante.username} - {self.nota}"