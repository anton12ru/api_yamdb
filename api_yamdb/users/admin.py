from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        *UserAdmin.fieldsets,
        ("Other Personal info", {"fields": ("role", "bio")}),
    )
