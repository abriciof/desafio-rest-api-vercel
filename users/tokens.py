from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmailTokenSerializer, VerifyEmailTokenSerializer
# from .utils.emailer import send_confirmation_email

User = get_user_model()


class SendEmailTokenView(APIView):
    """
    Gera um token de confirmação e envia para o e-mail do usuário.
    """
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    def post(self, request):
        serializer = EmailTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email__iexact=serializer.validated_data["email"])
        token = default_token_generator.make_token(user)
        # Envia e-mail com token (dentro do emailer você pode usar Django Email ou qualquer serviço)
        # send_confirmation_email(user.email, token)
        return Response({"detail": "Token enviado com sucesso."}, status=status.HTTP_200_OK)


class VerifyEmailTokenView(APIView):
    """
    Recebe e-mail + token, valida e marca o usuário como confirmado.
    """
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    def post(self, request):
        serializer = VerifyEmailTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]

        if not default_token_generator.check_token(user, token):
            return Response({"token": "Token inválido ou expirado."},
                            status=status.HTTP_400_BAD_REQUEST)

        user.email_confirmed = True
        user.save(update_fields=["email_confirmed"])
        return Response({"detail": "E-mail confirmado com sucesso."}, status=status.HTTP_200_OK)
