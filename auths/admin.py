from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from auths.models import Superuser, Blogger


# Register your models here.

class UserAdmin(BaseUserAdmin):
    search_fields = ['email', 'username', 'is_active', 'is_admin']
    readonly_fields = ['id', 'uuid', 'created_at', 'last_updated']
    list_display = ['first_name', 'last_name', 'email', 'username', 'is_active', 'is_admin', 'created_at']
    list_filter = ['is_active', 'is_admin', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = []


@admin.register(Superuser)
class Admin(UserAdmin):
    pass


@admin.register(Blogger)
class BloggerAdmin(UserAdmin):
    fieldsets = (
        (_('Bio Details'), {
            "fields": ["id", "uuid", "first_name", "last_name", "email", "username"]
        }),
        (_('Auth Details'), {
            "fields": ["is_active", "is_admin", "password"]
        }),
        (_('Dates'), {
            "fields": ["created_at", "last_updated"]
        }),
    )
