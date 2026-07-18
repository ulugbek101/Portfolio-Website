from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "display_name", "is_staff", "date_joined")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (_("Profile"), {"fields": ("avatar", "headline", "location")}),
    )
