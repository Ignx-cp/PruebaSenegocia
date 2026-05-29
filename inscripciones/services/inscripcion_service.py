from cursos.models import Curso

from inscripciones.models import Inscripcion

from inscripciones.exceptions import (
    CursoInactivoException,
    CursoSinCapacidadException,
    EstudianteYaInscritoException
)


class InscripcionService:

    @staticmethod
    def crear_inscripcion(estudiante, curso):

        if not curso.activo:
            raise CursoInactivoException()

        if Inscripcion.objects.filter(
            estudiante=estudiante,
            curso=curso
        ).exists():
            raise EstudianteYaInscritoException()

        cantidad_actual = Inscripcion.objects.filter(
            curso=curso
        ).count()

        if cantidad_actual >= curso.capacidad_maxima:
            raise CursoSinCapacidadException()

        return Inscripcion.objects.create(
            estudiante=estudiante,
            curso=curso
        )