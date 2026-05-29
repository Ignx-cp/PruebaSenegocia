from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    capacidad_maxima = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre