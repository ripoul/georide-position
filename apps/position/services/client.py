from datetime import datetime, timedelta

from django.conf import settings
from position.accounts.models import Profile, User
from rest_framework.test import APIClient


class GeorideClient(APIClient):
    def __init__(self, enforce_csrf_checks=False, **defaults):
        super().__init__(enforce_csrf_checks=enforce_csrf_checks, **defaults)
        email = settings.GEORIDE_EMAIL
        password = settings.GEORIDE_PASSWORD
        if email and password:
            self.user, _ = User.objects.get_or_create(
                username="georide_test_client", email=email, password=password
            )
            self.user.driver.get_new_token()
            tracker_ids = self.user.driver.get_trackers_id()
            start_date = datetime.now() - timedelta(days=10)
            end_date = datetime.now() + timedelta(days=10)
            Profile.objects.create_profile(
                self.user.username,
                self.user.email,
                self.user.password,
                self.user.token,
                tracker_ids[0][0],
                start_date,
                end_date,
            )
        else:
            self.user, _ = User.objects.get_or_create(
                username="georide_test_client",
                email="test.georide@gmail.com",
                password="incorrect",
            )
