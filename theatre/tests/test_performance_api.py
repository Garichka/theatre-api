import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theatre_config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from theatre.models import Play, TheatreHall, Performance

PERFORMANCE_URL = reverse("theatre:performance-list")


class PerformanceApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass"
        )
        self.client.force_authenticate(self.user)
        self.hall = TheatreHall.objects.create(name="Main", rows=10, seats_in_row=10)
        self.play = Play.objects.create(title="Test Play", description="Desc", duration=60)

    def test_list_performances(self):
        Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time="2024-01-01T12:00:00Z",
            price=10
        )
        res = self.client.get(PERFORMANCE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("tickets_available", res.data[0])
