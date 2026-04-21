import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theatre_config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from theatre.models import Play, TheatreHall, Performance, Reservation

RESERVATION_URL = reverse("theatre:reservation-list")


class ReservationApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass"
        )
        self.client.force_authenticate(self.user)
        self.hall = TheatreHall.objects.create(name="Small", rows=5, seats_in_row=5)
        self.play = Play.objects.create(title="P", description="D", duration=60)
        self.perf = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time="2024-01-01T12:00:00Z",
            price=10
        )

    def test_create_reservation_success(self):
        payload = {
            "tickets": [{"row": 1, "seat": 1, "performance": self.perf.id}]
        }
        res = self.client.post(RESERVATION_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_ticket_validation_invalid_row(self):
        payload = {
            "tickets": [{"row": 100, "seat": 1, "performance": self.perf.id}]
        }
        res = self.client.post(RESERVATION_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reservation_user_filtering(self):
        other_user = get_user_model().objects.create_user(
            email="other@test.com", password="password123"
        )
        Reservation.objects.create(user=other_user)
        res = self.client.get(RESERVATION_URL)
        self.assertEqual(len(res.data), 0)
