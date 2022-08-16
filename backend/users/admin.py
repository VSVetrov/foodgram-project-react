from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_filter = (
        'username', 'email', 'is_staff',
        'is_superuser', 'is_active', 'groups'
    )


admin.site.register(User, CustomUserAdmin)
