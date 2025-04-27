from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings

from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, BlacklistedToken
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    UserSerializer,
    LoginSerializer,
    TokenSerializer,
    EmailTokenSerializer,
    VerifyEmailTokenSerializer,
    GoogleAuthSerializer
)
from .utils.emailer import send_confirmation_email
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer
    http_method_names = ["post"]


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: TokenSerializer, 401: 'Credenciais inválidas'}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if not user:
            return Response(
                {"detail": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Gera e retorna só o access token
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Recebe o access token no Authorization header e revoga por JTI.
    """
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request):
        # extrai o token do header
        auth = request.headers.get("Authorization", "")
        if not auth.lower().startswith("bearer "):
            return Response(
                {"detail": _("Header Authorization 'Bearer <token>' obrigatório.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        token_str = auth.split()[1]

        # valida estrutura antes de extrair jti
        try:
            token = UntypedToken(token_str)
        except (InvalidToken, TokenError):
            return Response(
                {"detail": _("Token inválido.")},
                status=status.HTTP_401_UNAUTHORIZED
            )

        jti = token.get(api_settings.JTI_CLAIM)
        # grava no blacklist
        BlacklistedToken.objects.get_or_create(jti=jti)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SendEmailTokenView(APIView):
    """
    GET /api/auth/email/send-token/
    Gera e envia um token de confirmação para o e-mail do usuário logado.
    """
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request):
        user = request.user
        email = user.email

        # Gera o token único para este usuário
        token = default_token_generator.make_token(user)

        # Envia o e-mail (usa seu utilitário de SMTP configurado)
        send_confirmation_email(email, token)

        return Response(
            {"detail": "Token de confirmação enviado para o seu e-mail."},
            status=status.HTTP_200_OK
        )
    

class VerifyEmailTokenView(APIView):
    """
    GET /api/auth/email/verify-token/?email=<>&token=<>
    Verifica o token e marca email_confirmed=True.
    """
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description="E-mail cadastrado",
                type=openapi.TYPE_STRING,
                required=True
            ), openapi.Parameter(
                'token',
                openapi.IN_QUERY,
                description="Token de confirmação recebido por e-mail",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="OK",
                examples={"application/json": {"detail": "E-mail confirmado com sucesso."}}
            ),
            400: "Parâmetros inválidos ou token expirado.",
            404: "E-mail não cadastrado."
        }
    )
    def get(self, request):
        email = request.query_params.get("email")
        token = request.query_params.get("token")

        if not email or not token:
            return Response(
                {"detail": "Parâmetros 'email' e 'token' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "E-mail não cadastrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Token inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.email_confirmed = True
        user.save(update_fields=["email_confirmed"])

        return Response(
            {"detail": "E-mail confirmado com sucesso."},
            status=status.HTTP_200_OK
        )


class GoogleAuthView(APIView):
    """
    POST /api/auth/google/
    Body: { "id_token": "<JWT_emitido_pelo_Google>" }
    Retorna: { "token": "<seu_JWT_com_6h_de_vida>" }
    """
    authentication_classes = []       # sem JWT aqui
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post", "get"]

    @swagger_auto_schema(
        request_body=GoogleAuthSerializer,
        responses={200: TokenSerializer, 400: "Token inválido ou e-mail não verificado"}
    )
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token_str = serializer.validated_data["id_token"]

        # 1) valida o ID-Token junto ao Google
        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token_str,
                google_requests.Request(),
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )
        except ValueError:
            return Response(
                {"detail": "ID-Token do Google inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) somente permite e-mails verificados pelo Google
        if not idinfo.get("email_verified", False):
            return Response(
                {"detail": "E-mail não verificado pelo Google."},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = idinfo["email"]
        # 3) get_or_create do usuário local
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": idinfo.get("given_name", ""),
                "last_name": idinfo.get("family_name", ""),
                "profile_image": idinfo.get("picture", ""),
                "email_confirmed": True,   # já confirmado
            }
        )

        # 4) gera seu JWT padrão (6h)
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'token',
                openapi.IN_QUERY,
                description="Token gerado com OAuth2",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="OK",
                examples={"application/json": {"token": "token_gerado_com_oauth2"}}
            ),
            400: "Parâmetros inválidos.",
        }
    )
    def get(self, request):
        token = request.query_params.get("token")
        
        if token:
            return Response(
                {"token": str(token)}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Parâmetro 'token' é obrigatórios."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
