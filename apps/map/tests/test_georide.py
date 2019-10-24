import unittest

from django.test import TestCase
from hamcrest import assert_that, has_length, is_, not_none

from ..client import GeorideClient
from ..views import geo
from .fixtures import (
    GENERIC_SETUP_MESSAGE,
    GEORIDE_ACCOUNT_IS_SETUP,
    AccountsMixin,
    GeorideMixin,
)


@unittest.skipIf(GEORIDE_ACCOUNT_IS_SETUP, GENERIC_SETUP_MESSAGE)
class GeorideTestCase(TestCase, AccountsMixin, GeorideMixin):
    client_class = GeorideClient

    def test_get_token(self):
        token = geo.getNewToken(self.client.user.email, self.client.user.password)
        assert_that(token, is_(not_none()))

    @unittest.skip("Need to refactor geo")
    def test_get_token__incorrect_credentials(self):
        token = geo.getNewToken("test@gmail.com", "pass44")
        assert_that(token, is_(not_none()))

    def test_get_tracker_id(self):
        token = self.any_token(user=self.client.user)
        assert_that(token, is_(not_none()))
        tracker_id = geo.getTrackersID(token)
        assert_that(tracker_id, is_(not_none()))
