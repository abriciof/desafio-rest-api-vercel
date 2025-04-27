import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from items.models import Item

User = get_user_model()

class Command(BaseCommand):
    help = "Seed inicial de usuários e itens"

    def handle(self, *args, **options):
        if User.objects.filter(username="demo_user_1").exists():
            self.stdout.write(self.style.WARNING("Seed já foi executado."))
            return

        users = []
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f"demo_user_{i}",
                email=f"demo{i}@example.com",
                password="password123"
            )
            if i <= 2:
                user.email_confirmed = True
                user.save()
            users.append(user)

        self.stdout.write(self.style.SUCCESS("5 usuários criados!"))

        titles = [
            "Manual de Instalação",
            "Guia Avançado",
            "API para Iniciantes",
            "Checklist de Deploy",
            "RESTful API",
            "Documentação Técnica",
            "Política de Segurança",
            "Boas Práticas Django",
            "CRUD de Exemplo",
            "Swagger UI",
            "Migrations",
            "Padrões RESTful",
            "Tutorial de Swagger",
            "Integração com Google",
            "Pipeline de CI/CD",
            "Django",
            "Github",
            "Banco de Dados",
            "Modelo de Banco",
            "Testes Unitários",
            "Autenticação com JWT"
        ]

        for title in titles:
            Item.objects.create(
                owner=random.choice(users),
                title=title,
                body=f"Conteúdo completo sobre {title.lower()}...",
                is_draft=random.choice([True, False]),
                is_public=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS(f"{len(titles)} itens criados!"))
