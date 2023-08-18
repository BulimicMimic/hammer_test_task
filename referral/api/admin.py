from django.contrib import admin
from django.contrib.auth import get_user_model

from api.models import (
    AuthorizationCode,
)

EMPTY_VALUE = '--NONE--'

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone_number', 'user_invite_code', 'activated_code')
    search_fields = ('phone_number', 'user_invite_code', 'activated_code')
    empty_value_display = EMPTY_VALUE


@admin.register(AuthorizationCode)
class AuthorizationCodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'authorization_code')
    search_fields = ('user', 'authorization_code', )
    empty_value_display = EMPTY_VALUE
