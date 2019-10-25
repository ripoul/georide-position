from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from hamcrest import assert_that, has_length, is_, not_none

from ..models import Profile
from .fixtures import AccountsMixin


class ProfileModelTestCase(TestCase, AccountsMixin):
    def test_create_profile(self):
        """
        Given details for a profile
        When I try to create this profile for a pair (username, email, password) that does not exist
        Then I get a profile completed
        """
        user = self.any_user(save=False)
        token = "XXXX"
        tracker_id = 1
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)
        profile = Profile.objects.create_profile(
            username=user.username,
            email=user.email,
            password=user.password,
            token=token,
            tracker_id=tracker_id,
            start_date=start_date,
            end_date=end_date,
        )
        assert_that(profile, is_(not_none()))
        assert_that(profile.user, is_(not_none()))
        assert_that(profile.tracker_id, is_(tracker_id))
        assert_that(profile.start_date, is_(start_date))
        assert_that(profile.end_date, is_(end_date))
