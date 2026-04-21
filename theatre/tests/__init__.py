import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theatre_config.settings")
django.setup()

from rest_framework.test import APITestCase, APIClient
