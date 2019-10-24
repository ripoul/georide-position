import unittest

from django.test import TestCase
from hamcrest import assert_that, has_length, is_, not_none, none

from ..client import GeorideClient
from ..driver import GeorideDriver
from .fixtures import (
    GeorideMixin,
)
from . import GENERIC_SETUP_MESSAGE, GEORIDE_ACCOUNT_IS_SETUP


@unittest.skipIf(GEORIDE_ACCOUNT_IS_SETUP, GENERIC_SETUP_MESSAGE)
class GeorideTestCase(TestCase, GeorideMixin):
    client_class = GeorideClient

    def test_get_token(self):
        token = self.client.user.driver.getNewToken()
        assert_that(token, is_(not_none()))

    @unittest.skip("Need to refactor geo")
    def test_get_token__incorrect_credentials(self):
        token = geo.getNewToken("test@gmail.com", "pass44")
        assert_that(token, is_(not_none()))

    def test_get_tracker_id(self):
        token = self.any_token(user=self.client.user)
        assert_that(token, is_(not_none()))
        trackers = geo.getTrackersID(token)
        assert_that(trackers, is_(not_none()))

    @unittest.skip("Need to refactor geo")
    def test_get_tracker_id__incorrect_token(self):
        token = 'unauthenticated'
        trackers = geo.getTrackersID(token)
        assert_that(trackers, is_(none()))

    def test_get_position(self):
        token = self.any_token(user=self.client.user)
        response = geo.getTrackersID(token)
        assert_that(response, is_(not_none()))
        import ipdb; ipdb.set_trace()
        pass

