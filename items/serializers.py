from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id", "title", "body", "is_public", "is_draft",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
