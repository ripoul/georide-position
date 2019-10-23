from django.conf import settings
from django.contrib.auth import get_user_model

from ..models import Profile

User = get_user_model()


GEORIDE_ACCOUNT_IS_SETUP = not settings.GEORIDE_EMAIL and not settings.GEORIDE_PASSWORD
GENERIC_SETUP_MESSAGE = (
    "export GEORIDE_EMAIL and GEORIDE_PASSWORD environment variables to run this test"
)


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
