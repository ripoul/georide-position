from django.conf import settings

GEORIDE_ACCOUNT_IS_SETUP = False
GENERIC_SETUP_MESSAGE = (
    "Running test with incorrect settings file please use test_settings instead"
)

if hasattr(settings, "GEORIDE_EMAIL") and hasattr(settings, "GEORIDE_PASSWORD"):
    GEORIDE_ACCOUNT_IS_SETUP = (
        not settings.GEORIDE_EMAIL and not settings.GEORIDE_PASSWORD
    )
    GENERIC_SETUP_MESSAGE = "export GEORIDE_EMAIL and GEORIDE_PASSWORD environment variables to run this test"
