from cursos.models import Curso


class CursoService:

    @staticmethod
    def listar():
        return Curso.objects.all().order_by("id")

    @staticmethod
    def obtener_por_id(curso_id):
        return Curso.objects.get(id=curso_id)