# Database models

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    # Manager for Users

    def create_user(self, email, password=None, **extra_fields):
        # Create, Save and return a new user
        if not email:
            raise ValueError("User must have an Email address!")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        #  ^ best practice to save user in case there are multiple dbs

        return user

    def create_superuser(self, email, password):
        # Create and return a new superuser
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # User in the system
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # How to connect a Model Manager to a model

    USERNAME_FIELD = 'email'


class Recipe(models.Model):  # models.Model is base Model Class
    """Recipe Object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Connect User Model to Recipe Model
        on_delete=models.CASCADE,  # If User Delete, Delete the recipes linked
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")  # Multiple Tags connected to Recipe

    def __str__(self):  # String Representation of recipe (to_string in java)
        return self.title

class Tag(models.Model):
    """Tag Model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name