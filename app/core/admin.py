# Django Admin Customization

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as translate

from core import models


class UserAdmin(BaseUserAdmin):
    # Define the admin pages for users
    ordering = ["id"]
    list_display = ["email", "name"]

    # Supporting CRUD
    fieldsets = (
        (None,  {"fields": ("email", "password")}),
        (translate("Personal Info"), {"fields": ("name",)}),
        (
            translate("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            }
        ),
        (translate("Important Dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]  # makes last_login field readonly

    add_fieldsets = (
        (None, {
            "classes": ("wide",),  # Class (wide) adds slight change with css
            "fields": (
                "email",
                "password1",
                "password2",
                "name",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )


"""
Adds User Model to the Admin Page, we format it using our custom
User Admin which we type as the second parameter, otherwise it would
use Django's default useradmin which we said is "BaseUserAdmin"
"""
admin.site.register(models.User, UserAdmin)
