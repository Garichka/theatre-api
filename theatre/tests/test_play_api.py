import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theatre_config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from theatre.models import Genre, Actor, Play
from theatre.serializers import PlayListSerializer

PLAY_URL = reverse("theatre:play-list")


class PlayApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass"
        )
        self.client.force_authenticate(self.user)

    def test_list_plays(self):
        Play.objects.create(title="Play 1", description="Description", duration=100)
        res = self.client.get(PLAY_URL)
        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_plays_by_genres(self):
        genre = Genre.objects.create(name="Drama")
        play = Play.objects.create(title="Drama Play", description="Desc", duration=90)
        play.genres.add(genre)
        res = self.client.get(PLAY_URL, {"genres": f"{genre.id}"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_filter_plays_by_actors(self):
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        play = Play.objects.create(title="Actor Play", description="Desc", duration=90)
        play.actors.add(actor)
        res = self.client.get(PLAY_URL, {"actors": f"{actor.id}"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
