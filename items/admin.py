from django.contrib import admin
from .models import *

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('owner','title','body','is_public','is_draft','created_at','updated_at')
    list_filter = ('owner','is_public','is_draft','created_at','updated_at')
    search_fields = ('title','body')
