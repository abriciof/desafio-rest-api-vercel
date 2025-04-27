import os
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
import vercel_blob

class UploadImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_description="Faz upload de uma imagem (até 4 MB) e retorna a URL no storage.",
        manual_parameters=[
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Imagem para upload (JPEG, PNG, até 4 MB)",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Upload realizado com sucesso",
                examples={"application/json": {"url": "https://link-do-blob-storage"}}
            ),
            400: "Erro de validação ou upload inválido"
        }
    )
    def post(self, request):
        file_obj = request.FILES.get("image")
        if not file_obj:
            return Response({"detail": "Arquivo não enviado."}, status=status.HTTP_400_BAD_REQUEST)

        if not file_obj.content_type.startswith('image/'):
            return Response({"detail": "O arquivo deve ser uma imagem (JPEG, PNG, etc)."}, status=status.HTTP_400_BAD_REQUEST)

        max_size_mb = 4
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_obj.size > max_size_bytes:
            return Response({"detail": f"Tamanho máximo permitido é {max_size_mb} MB."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blob = vercel_blob.put(
                file_obj.name,
                file_obj.read(),
                {}
            )

            if blob.__contains__('url'):
                return Response({'url': blob['url']}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Erro ao receber imagem no Blob, tente novamente mais tarde."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
