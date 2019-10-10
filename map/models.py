from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedTextField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # name, email, password
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    token = EncryptedTextField()
