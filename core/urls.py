from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.views.generic import RedirectView, TemplateView
from .settings import GOOGLE_OAUTH2_CLIENT_ID

schema_view = get_schema_view(
    openapi.Info(
        title="Desafio API RESTful",
        default_version="v1",
        description="API com registro, JWT, Google OAuth2, listagens públicas e restritas",
    ),
    public=True,
    authentication_classes=(),
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Área de Admin
    path("admin/", admin.site.urls),
    
    # Login com o Google
    path(
        "login-google/", 
        TemplateView.as_view(
            template_name="login-google.html",
            extra_context={"GOOGLE_OAUTH2_CLIENT_ID": GOOGLE_OAUTH2_CLIENT_ID}
        ), name="login-google"
    ),
    path(
        "login-callback/", 
        TemplateView.as_view(
            template_name="login-google-callback.html"
        ), name="login-callback"
    ),

    # Endpoints da API
    path("api/auth/", include("users.urls_auth")),
    path("api/users/", include("users.urls_profile")),
    path("api/items/", include("items.urls")),

    # Swagger e Redoc
    path("", RedirectView.as_view(url="swagger/")),
    path("swagger(<format>\.json|\.yaml)",schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # Termos de Uso e Política de Privacidade
    path("api/docs/", include("common.urls")),
]
