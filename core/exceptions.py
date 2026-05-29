import logging

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        logger.warning(
            "Handled API exception",
            extra={
                "status_code": response.status_code,
                "view": context.get("view").__class__.__name__ if context.get("view") else None,
                "exception": exc.__class__.__name__,
            },
        )

        return Response(
            {
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "detail": response.data,
                },
            },
            status=response.status_code,
        )

    logger.exception(
        "Unhandled API exception",
        extra={
            "view": context.get("view").__class__.__name__ if context.get("view") else None,
            "exception": exc.__class__.__name__,
        },
    )

    return Response(
        {
            "success": False,
            "error": {
                "type": "InternalServerError",
                "detail": "Ocurrió un error interno en el servidor.",
            },
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )