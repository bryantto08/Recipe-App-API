"""
URL Mappings for the recpe app
"""
from django.urls import (
    path, include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)  # Auto-generate endpoints for each options in viewset

app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),
]

