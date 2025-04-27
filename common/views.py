import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


DOCS_DIR = os.path.join(settings.BASE_DIR, "docs")

class TermsOfUseView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_description="Retorna o PDF de Termos de Uso",
        responses={200: openapi.Response('application/pdf')}
    )
    def get(self, request):
        path = os.path.join(DOCS_DIR, "terms_of_use.pdf")
        if not os.path.exists(path):
            raise Http404("PDF de Termos de Uso não encontrado.")
        
        response = FileResponse(open(path, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="terms_of_use.pdf"'
        return response


class PrivacyPolicyView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    @swagger_auto_schema(
        operation_description="Retorna o PDF de Política de Privacidade",
        responses={200: openapi.Response('application/pdf')}
    )
    def get(self, request):
        path = os.path.join(DOCS_DIR, "privacy_policy.pdf")
        if not os.path.exists(path):
            raise Http404("PDF de Política de Privacidade não encontrado.")
        
        response = FileResponse(open(path, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="privacy_policy.pdf"'
        return response
