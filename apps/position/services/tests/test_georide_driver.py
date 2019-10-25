import unittest

from django.conf import settings
from django.test import TestCase
from hamcrest import (
    assert_that,
    greater_than,
    has_length,
    instance_of,
    is_,
    none,
    not_none,
)
from position.accounts.tests.fixtures import AccountsMixin
from rest_framework.exceptions import ValidationError

from . import GENERIC_SETUP_MESSAGE, GEORIDE_ACCOUNT_IS_SETUP
from ..client import GeorideClient
from ..driver import GeorideDriver, georide_unauthenticated_driver
from .fixtures import GeorideMixin


@unittest.skipIf(GEORIDE_ACCOUNT_IS_SETUP, GENERIC_SETUP_MESSAGE)
class GeorideUnauthenticatedDriverTestCase(TestCase, GeorideMixin, AccountsMixin):
    def test_get_token(self):
        token = georide_unauthenticated_driver.get_new_token(
            email=settings.GEORIDE_EMAIL, password=settings.GEORIDE_PASSWORD
        )
        assert_that(token, is_(not_none()))

    def test_get_token__incorrect_credentials(self):
        with self.assertRaises(ValidationError):
            georide_unauthenticated_driver.get_new_token(
                email=settings.GEORIDE_EMAIL, password="toto44"
            )

    def test_get_tracker_ids(self):
        token = self.any_token()
        assert_that(token, is_(not_none()))
        tracker_ids = georide_unauthenticated_driver.get_trackers_id(token)
        assert_that(tracker_ids, is_(not_none()))
        assert_that(tracker_ids, has_length(greater_than(0)))
        assert_that(tracker_ids, is_(instance_of(list)))
        assert_that(tracker_ids[0], has_length(2))
        assert_that(tracker_ids[0], is_(instance_of(list)))

    def test_get_tracker_id__incorrect_token(self):
        with self.assertRaises(ValidationError):
            georide_unauthenticated_driver.get_trackers_id("incorrect")
