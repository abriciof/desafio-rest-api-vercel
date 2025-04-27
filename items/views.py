from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Item
from .serializers import ItemSerializer


class ItemListView(generics.ListAPIView):
    queryset = Item.objects.filter(is_public=True)
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_draft"]       # ?is_draft=True
    search_fields = ["title", "body"]     # ?search=termo
    ordering_fields = ["created_at", "title"]  # ?ordering=-created_at
    http_method_names = ["get"]


class ItemRestrictedListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_draft"]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "title"]
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        if not request.user.email_confirmed:
            raise PermissionDenied("E-mail não confirmado.")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Item.objects.all()
