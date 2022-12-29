# Tests for Django Admin modifications

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    # Tests for the Django Admin

    def setUp(self):
        # Create user and client
        
        self.client = Client()  # Superuser account
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(  # Regular user account
            email="user@example.com",
            password="testpass123",
            name="Test User"
        )

    def test_users_list(self):
        # Tests that useres are listed on page
        url = reverse("admin:core_user_changelist")  # get url from admin page that shows list of users
        res = self.client.get(url) 

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)