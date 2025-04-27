from django.urls import path
from .views import ItemListView, ItemRestrictedListView

urlpatterns = [
    path("", ItemListView.as_view(), name="items-public"),
    path("restricted/", ItemRestrictedListView.as_view(), name="items-restricted"),
]
