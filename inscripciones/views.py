from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Inscripcion
from .serializers import InscripcionSerializer

from .services.inscripcion_service import InscripcionService

from .exceptions import (
    CursoInactivoException,
    CursoSinCapacidadException,
    EstudianteYaInscritoException
)


class InscripcionViewSet(ModelViewSet):

    queryset = Inscripcion.objects.all()

    serializer_class = InscripcionSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            inscripcion = (
                InscripcionService.crear_inscripcion(
                    serializer.validated_data["estudiante"],
                    serializer.validated_data["curso"]
                )
            )

            return Response(
                InscripcionSerializer(
                    inscripcion
                ).data,
                status=status.HTTP_201_CREATED
            )

        except CursoInactivoException:

            return Response(
                {
                    "detail":
                    "El curso está inactivo."
                },
                status=status.HTTP_409_CONFLICT
            )

        except CursoSinCapacidadException:

            return Response(
                {
                    "detail":
                    "El curso alcanzó su capacidad máxima."
                },
                status=status.HTTP_409_CONFLICT
            )

        except EstudianteYaInscritoException:

            return Response(
                {
                    "detail":
                    "El estudiante ya está inscrito."
                },
                status=status.HTTP_409_CONFLICT
            )