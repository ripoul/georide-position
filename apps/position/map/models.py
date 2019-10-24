from django.contrib.auth.models import User
from django.db import models
from fernet_fields import EncryptedTextField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class GeorideUser(User):

    class Meta:
        proxy = True

    @property
    def driver(self):
        from position.services.driver import GeorideDriver
        return GeorideDriver(self)



class ProfileManager(models.Manager):
    def create_profile(
        self, username, email, password, token, trackerID, startDate, endDate
    ):
        user, _ = User.objects.get_or_create(
            username=username, email=email, password=password
        )
        profile, _ = self.get_or_create(
            user=user,
            defaults={
                'startDate': startDate,
                'endDate': endDate,
                'token': token,
                'trackerID': trackerID
            }
        )
        return profile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    token = EncryptedTextField()
    trackerID = models.IntegerField()

    objects = ProfileManager()


