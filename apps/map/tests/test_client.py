import unittest

from django.test import TestCase
from hamcrest import assert_that, is_, not_none

from . import GENERIC_SETUP_MESSAGE, GEORIDE_ACCOUNT_SETUP
from ..client import GeorideClient


@unittest.skipIf(GEORIDE_ACCOUNT_SETUP, GENERIC_SETUP_MESSAGE)
class GeorideClientTestCase(TestCase):
    def test_init_client(self):
        client = GeorideClient()
        assert_that(client.user, is_(not_none()))
