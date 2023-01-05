"""
URL Mappings for the recipe app
"""
from django.urls import (
    path, include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)  # Auto-generate endpoints for each options in viewset
router.register("tags", views.TagViewSet)  # Auto-generated endpoint
router.register("ingredients", views.IngredientViewSet)
app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]

