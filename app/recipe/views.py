"""
Views for the Recipe APIs
"""

from drf_spectacular.utils import (  # For specific query apis
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


# Making a Base Class for TagViewSet and Ingredients ViewSet
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "assigned_only",
                OpenApiTypes.INT, enum=[0, 1],
                description="Filter by items assigned to recipes"
            )
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes"""
    authentication_classes = [TokenAuthentication]  # Supports Token Auth
    permission_classes = [IsAuthenticated]  # Need to be Auth to use API

    # Custom Method so we don't get recipes from other users
    def get_queryset(self):
        """Retrieve Tags for authenticated user"""
        assigned_only = bool(
            int(self.request.query_params.get("assigned_only", 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by("-name").distinct()


@extend_schema_view(  # Extend auto-generated schema by drf spectacular
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "tags",
                OpenApiTypes.STR,
                description="Comma separated list of IDs to filter"
            ),
            OpenApiParameter(
                "ingredients",
                OpenApiTypes.STR,
                description="Comma separated list of ingredients to filter"
            )
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]  # Supports Token Auth
    permission_classes = [IsAuthenticated]  # Need to be Auth to use API

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers [1, 2, 3]"""
        return [int(str_id) for str_id in qs.split(",")]

    # Custom Method So we don't get recipes from other users
    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        queryset = self.queryset  # Original queryset
        if tags:  # Editing it so it filters by tag and ingredients
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        # Return the NEW queryset (only from current user)
        return queryset.filter(
            user=self.request.user
        ).order_by("-id").distinct()

    def get_serializer_class(self):  # Figuring out with serializer to use
        """Return the serializer class for request"""
        if self.action == "list":  # Default Action in viewset
            return serializers.RecipeSerializer  # reference to class
        elif self.action == "upload_image":   # Custom Action we create
            return serializers.RecipeImageSerializer
        return self.serializer_class

    """
    We call this function everytime we call the create_recipe function
    """
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    """
    Custom Action, only expect HTTP Post request,
    detail=True (specific object, not list)
    """
    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():  # If ImageSerializer
            serializer.save()  # Save into DB
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage Ingredients in the DB"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
