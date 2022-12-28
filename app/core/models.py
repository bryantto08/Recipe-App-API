# Database models

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
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        #  ^ best practice to save user in case there are multiple dbs

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # User in the system
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # How to connect a Model Manager to a model

    USERNAME_FIELD = 'email'
