from rest_framework.permissions import BasePermission


class EsAdministrador(BasePermission):
    message = "Solo los administradores pueden realizar esta acción."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.rol == "ADMINISTRADOR"
        )