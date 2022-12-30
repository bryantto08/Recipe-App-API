"""
URL Mappings for the user API
"""
from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    # name connects 
    path("create/", views.CreateUserView.as_view(), name="create"),
]
