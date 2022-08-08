from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


class CustomUserAdmin(UserAdmin):
    list_filter = (
        'username', 'email', 'is_staff',
        'is_superuser', 'is_active', 'groups'
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'