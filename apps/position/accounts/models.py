from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from fernet_fields import EncryptedTextField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )
    email = models.EmailField()
    token = EncryptedTextField(blank=True, null=True)

    USERNAME_FIELD = "username"

    @property
    def driver(self):
        from position.services.driver import GeorideDriverAuthenticated

        return GeorideDriverAuthenticated(self)


class ProfileManager(models.Manager):
    def create_profile(
        self, username, email, password, token, tracker_id, start_date, end_date
    ):
        user, _ = User.objects.get_or_create(
            username=username, email=email, defaults={"token": token}
        )
        profile, _ = self.get_or_create(
            user=user,
            defaults={
                "start_date": start_date,
                "end_date": end_date,
                "tracker_id": tracker_id,
            },
        )
        return profile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    tracker_id = models.IntegerField()

    objects = ProfileManager()
