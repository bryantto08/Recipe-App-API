"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create") 
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()  # API Client: What we use to access the APIs
    
    def test_create_user_success(self):
        """ Test creating the user is successful"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }

        # HTTP Post Request to /user/create endpoint with payload
        res = self.client.post(CREATE_USER_URL, payload)

        # Success Create HTTP Response 201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Grabs user from database using objects.get and the email
        user = get_user_model().objects.get(email=payload["email"])
        # Checks if its the correct user by checking the password
        self.assertTrue(user.check_password(payload["password"]))
        # No Password in the api response
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test Name",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Test an error is returned if password less than 5 chars."""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if user exists: returns boolean
        user_exists = get_user_model().objects.filter(
            email = payload["email"]
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""
        user_details = {  # Creating a User
            "name": "Test Name",
            "email" : "test@example.com",
            "password": "test-user-password123",
        }
        create_user(**user_details)

        payload = {  # Payload that will be sent to API
            "email" : user_details["email"],
            "password" : user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)  # Theres a token attribute in res
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""
        create_user(email="test@example.com", password="goodpass")
        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email":"test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)