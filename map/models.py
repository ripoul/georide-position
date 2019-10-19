from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedTextField


class ProfileManager(models.Manager):
    def create_profile(
        self, username, email, password, token, trackerID, startDate, endDate
    ):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        try:
            profile = self.create(
                user=user,
                startDate=startDate,
                endDate=endDate,
                token=token,
                trackerID=trackerID,
            )
        except Exception as e:
            u = User.objects.get(username=username)
            u.delete()
            raise e
        # do something with the book
        return profile


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # name, email, password
    startDate = models.DateField()
    endDate = models.DateField()
    token = EncryptedTextField()
    trackerID = models.IntegerField()

    objects = ProfileManager()
