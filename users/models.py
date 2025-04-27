from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField("E-mail", unique=True)
    first_name = models.CharField("Nome", max_length=150, blank=True)
    last_name = models.CharField("Sobrenome", max_length=150, blank=True)
    profile_image = models.URLField("Foto de Perfil", blank=True, null=True)
    email_confirmed = models.BooleanField("E-mail confirmado?", default=False)

    def __str__(self):
        return self.username


class BlacklistedToken(models.Model):
    jti = models.CharField("JTI do token", max_length=255, unique=True)
    blacklisted_at = models.DateTimeField("Revogado em", auto_now_add=True)

    def __str__(self):
        return self.jti