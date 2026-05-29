from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from cursos.models import Curso
from inscripciones.models import Inscripcion
from evaluaciones.models import Evaluacion


Usuario = get_user_model()


class EvaluacionAPITestCase(APITestCase):
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
            nombre="Python",
            descripcion="Curso Python",
            capacidad_maxima=10,
            activo=True,
        )

        self.inscripcion = Inscripcion.objects.create(
            estudiante=self.estudiante,
            curso=self.curso,
        )

    def test_crear_evaluacion_exitosa(self):
        response = self.client.post(
            "/api/evaluaciones/",
            {
                "inscripcion": self.inscripcion.id,
                "nota": 6.5,
                "observacion": "Buen desempeño",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Evaluacion.objects.count(), 1)

    def test_no_permite_nota_menor_a_uno(self):
        response = self.client.post(
            "/api/evaluaciones/",
            {
                "inscripcion": self.inscripcion.id,
                "nota": 0.5,
                "observacion": "Nota inválida",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_permite_nota_mayor_a_siete(self):
        response = self.client.post(
            "/api/evaluaciones/",
            {
                "inscripcion": self.inscripcion.id,
                "nota": 7.5,
                "observacion": "Nota inválida",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lista_evaluacion_con_estudiante_y_curso(self):
        Evaluacion.objects.create(
            inscripcion=self.inscripcion,
            nota=6.0,
            observacion="Correcto",
        )

        response = self.client.get("/api/evaluaciones/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resultado = response.data["results"][0]
        self.assertIn("estudiante", resultado)
        self.assertIn("curso", resultado)