# Django Admin Customization

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

class UserAdmin(BaseUserAdmin):
    # Define the admin pages for users
    ordering = ["id"]
    list_display = ["email", "name"]

"""
Adds User Model to the Admin Page, we format it using our custom 
User Admin which we type as the second parameter, otherwise it would
use Django's default useradmin which we said is "BaseUserAdmin"
"""
admin.site.register(models.User, UserAdmin)