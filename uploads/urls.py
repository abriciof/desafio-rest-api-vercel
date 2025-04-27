from django.urls import path
from .views import UploadImageView

urlpatterns = [
    path("image/", UploadImageView.as_view(), name="upload-image"),
]
