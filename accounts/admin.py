from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "role_name", "display_name")
    search_fields = ("role_name", "display_name")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "department", "is_staff", "is_superuser")
    list_filter = ("role", "department", "is_staff", "is_superuser")
    search_fields = ("username", "email")
