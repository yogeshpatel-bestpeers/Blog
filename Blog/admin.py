# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Blog, Category, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "first_name", "last_name"]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "status", "created_at"]
    list_filter = ["status"]
    actions = ["approve_blogs"]

    def approve_blogs(self, request, queryset):
        queryset.update(status="approved")


admin.site.register(Category)
