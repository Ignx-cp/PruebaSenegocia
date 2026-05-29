from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from cursos.models import Curso
from inscripciones.models import Inscripcion
from evaluaciones.models import Evaluacion


Usuario = get_user_model()


class ReportesAPITestCase(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username="admin",
            password="admin123",
            rol=Usuario.Roles.ADMINISTRADOR,
        )

        self.estudiante = Usuario.objects.create_user(
            username="estudiante",
            password="test123",
            rol=Usuario.Roles.ESTUDIANTE,
        )

        self.client.force_authenticate(user=self.admin)

        self.curso = Curso.objects.create(
            nombre="Django",
            descripcion="Curso Django",
            capacidad_maxima=5,
            activo=True,
        )

        self.inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            curso=self.curso,
        )

        Evaluacion.objects.create(
            inscripcion=self.inscripcion,
            nota=6.0,
            observacion="Buen trabajo",
        )

    def test_reporte_cursos_inscritos(self):
        response = self.client.get("/api/reportes/cursos-inscritos/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["cantidad_inscritos"], 1)

    def test_reporte_cupos_disponibles(self):
        response = self.client.get("/api/reportes/cupos-disponibles/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["inscritos"], 1)
        self.assertEqual(response.data[0]["cupos_disponibles"], 4)

    def test_reporte_promedio_notas(self):
        response = self.client.get("/api/reportes/promedio-notas/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data[0]["promedio_notas"]), 6.0)