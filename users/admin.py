from django.contrib import admin, auth

User = auth.get_user_model()
# Register your models here.
@admin.register(User)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('username','email','first_name','last_name')
