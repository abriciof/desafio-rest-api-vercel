from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    ChangePasswordView, 
    LogoutView, 
    SendEmailTokenView, 
    VerifyEmailTokenView,
    GoogleAuthView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
    path("google/", GoogleAuthView.as_view(), name="auth-google"),

    # Verificação de Email
    path("email/send-token/", SendEmailTokenView.as_view(), name="email-send-token"),
    path("email/verify-token/", VerifyEmailTokenView.as_view(), name="email-verify-token"),

]
