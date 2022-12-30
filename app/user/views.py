"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new aut token for user"""
    serializer_class = AuthTokenSerializer
    rendered_classes = api_settings.DEFAULT_RENDERER_CLASSES  # Browsable API

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the Authenticated User"""
    serializer_class = UserSerializer
    # Authentication: Is the user who they say they are
    # Permissions: What is the user allowed to do
    # We auth using TokenAuth, Only requirement for permission is Auth
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user