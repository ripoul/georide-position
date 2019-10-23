from django.conf import settings

GEORIDE_ACCOUNT_SETUP = not settings.GEORIDE_EMAIL and not settings.GEORIDE_PASSWORD
GENERIC_SETUP_MESSAGE = (
    "export GEORIDE_EMAIL and GEORIDE_PASSWORD environment variables to run this test"
)
