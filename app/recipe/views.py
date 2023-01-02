"""
Views for the Recipe APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]  # Supports Token Auth
    permission_classes = [IsAuthenticated]  # Need to be Auth to use API

    def get_queryset(self):  # Custom Method So we don't get recipes from other users
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):  # Figuring out with serializer to use
        """Return the serializer class for request"""
        if self.action == "list":
            return serializers.RecipeSerializer  # reference to class, NOT object
        return self.serializer_class

    """
    We call this function everytime we call the create_recipe function
    """
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

