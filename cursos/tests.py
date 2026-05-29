from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from cursos.models import Curso

Usuario = get_user_model()


class CursoAPITestCase(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_user(
            username="admin",
            password="admin123",
            rol=Usuario.Roles.ADMINISTRADOR,
        )

        self.client.force_authenticate(user=self.admin)

    def test_crear_curso(self):
        response = self.client.post(
            "/api/cursos/",
            {
                "nombre": "Python",
                "descripcion": "Curso Python",
                "capacidad_maxima": 20,
                "activo": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curso.objects.count(), 1)

    def test_listar_cursos(self):
        Curso.objects.create(
            nombre="Django",
            descripcion="Curso Django",
            capacidad_maxima=10,
            activo=True,
        )

        response = self.client.get("/api/cursos/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)