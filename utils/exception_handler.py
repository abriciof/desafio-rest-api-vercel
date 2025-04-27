from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ParseError):
        return Response(
            {"detail": "Corpo da requisição inválido: JSON mal-formado."},
            status=status.HTTP_400_BAD_REQUEST
        )

    return response
