from django.urls import path
from .views import TermsOfUseView, PrivacyPolicyView

urlpatterns = [
    path("terms/", TermsOfUseView.as_view(), name="terms-of-use"),
    path("privacy/", PrivacyPolicyView.as_view(), name="privacy-policy"),
]