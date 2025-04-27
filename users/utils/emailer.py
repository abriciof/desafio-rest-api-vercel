from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_confirmation_email(to_email: str, token: str):
    subject = "Confirme seu e-mail"

    confirm_url = (
        f"{settings.API_BASE_URL}/api/auth/email/verify-token/"
        f"?email={to_email}&token={token}"
    )
    
    message = (
        f"Olá!\n\n"
        f"Para confirmar seu e-mail, acesse:\n\n"
        f"{confirm_url}\n\n"
        f"Se você não solicitou este e-mail, pode ignorar."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )