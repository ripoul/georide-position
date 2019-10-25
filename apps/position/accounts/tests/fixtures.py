from django.conf import settings
from django.contrib.auth import get_user_model
from position.maps.views import geo
from position.services.client import GeorideClient

from ..models import Profile

User = get_user_model()


class AccountsMixin(object):
    def any_user(
        self,
        username="test_user",
        password="toto_44",
        email="test_user@gmail.com",
        save=True,
    ):
        user = User(username=username, password=password, email=email)
        if save:
            user.save()
        return user
