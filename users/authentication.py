from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import BlacklistedToken

class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)
        jti = validated_token.get("jti")
        if BlacklistedToken.objects.filter(jti=jti).exists():
            raise AuthenticationFailed("Este token foi revogado.")
        return validated_token
