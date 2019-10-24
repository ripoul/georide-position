from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


class GeorideClient(APIClient):
    def __init__(self, enforce_csrf_checks=False, **defaults):
        super().__init__(enforce_csrf_checks=enforce_csrf_checks, **defaults)
        email = settings.GEORIDE_EMAIL
        password = settings.GEORIDE_PASSWORD
        if email and password:
            self.user, _ = User.objects.get_or_create(
                username="georide_test_client", email=email, password=password
            )
        else:
            self.user, _ = User.objects.get_or_create(
                username="georide_test_client",
                email="test.georide@gmail.com",
                password="incorrect",
            )
