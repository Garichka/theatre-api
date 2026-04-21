import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theatre_config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

CREATE_USER_URL = reverse("user:register")
TOKEN_URL = reverse("user:token")


class UserApiTests(APITestCase):
    def test_create_user_success(self):
        payload = {
            "email": "test@example.com",
            "password": "testpassword123",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_with_short_password_error(self):
        payload = {
            "email": "test@example.com",
            "password": "123",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_success(self):
        email = "test@example.com"
        password = "testpassword123"
        get_user_model().objects.create_user(email=email, password=password)

        payload = {
            "username": email,
            "password": password,
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        get_user_model().objects.create_user(
            email="test@example.com",
            password="testpassword123"
        )

        payload = {"username": "test@example.com", "password": "wrongpassword"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
