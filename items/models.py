from django.db import models
from django.conf import settings

class Item(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items"
    )
    title = models.CharField("Título", max_length=255)
    body = models.TextField("Conteúdo")
    is_public = models.BooleanField("Público?", default=True)
    is_draft = models.BooleanField("Rascunho?", default=False)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.title
