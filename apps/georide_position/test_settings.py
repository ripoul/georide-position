# flake8: noqa
from georide_position.settings import *

DEBUG = True

# Use a fast hasher to speed up tests.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Georide Configuration

GEORIDE_EMAIL = os.getenv("GEORIDE_EMAIL", None)
GEORIDE_PASSWORD = os.getenv("GEORIDE_PASSWORD", None)
