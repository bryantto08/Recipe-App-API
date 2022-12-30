"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

# Serializers: Way to convert Input(JSON) to Python Object or Model
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]  # Fields that user can change
        extra_kwargs = {"password" : { "write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """ Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """valid and authenticate the user"""
        email = attrs.get("email")  # retrieve email and pass from view
        password = attrs.get("password")
        user = authenticate(  # built in method; check if username and pass are correct
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:  # If authenticatio failed (return None)
            msg = _("Unable to authenicate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")
            # View will translate this into HTTP 400 response ^
        attrs["user"] = user
        return attrs

