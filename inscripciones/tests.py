from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from cursos.models import Curso
from inscripciones.models import Inscripcion


Usuario = get_user_model()


class InscripcionAPITestCase(APITestCase):
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
            nombre="Django REST Framework",
            descripcion="Curso de DRF",
            capacidad_maxima=1,
            activo=True,
        )

    def test_crear_inscripcion_exitosa(self):
        response = self.client.post(
            "/api/inscripciones/",
            {
                "estudiante": self.estudiante.id,
                "curso": self.curso.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Inscripcion.objects.count(), 1)

    def test_no_permite_inscripcion_duplicada(self):
        Inscripcion.objects.create(
            estudiante=self.estudiante,
            curso=self.curso,
        )

        response = self.client.post(
            "/api/inscripciones/",
            {
                "estudiante": self.estudiante.id,
                "curso": self.curso.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_no_permite_inscripcion_si_curso_inactivo(self):
        curso_inactivo = Curso.objects.create(
            nombre="Curso inactivo",
            descripcion="No disponible",
            capacidad_maxima=10,
            activo=False,
        )

        response = self.client.post(
            "/api/inscripciones/",
            {
                "estudiante": self.estudiante.id,
                "curso": curso_inactivo.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_no_permite_inscripcion_si_no_hay_cupos(self):
        Inscripcion.objects.create(
            estudiante=self.estudiante,
            curso=self.curso,
        )

        otro_estudiante = Usuario.objects.create_user(
            username="otro_estudiante",
            password="test123",
            rol=Usuario.Roles.ESTUDIANTE,
        )

        response = self.client.post(
            "/api/inscripciones/",
            {
                "estudiante": otro_estudiante.id,
                "curso": self.curso.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)