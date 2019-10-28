from contextlib import contextmanager

import requests

__all__ = ["handle_georide_api_http_error", "georide_exceptions"]


class GeorideAPIException(Exception):
    status = 502

    def __init__(self, message):
        self.main_message = message


class GeorideAPIUnauthoriedException(GeorideAPIException):
    def __init__(self, message="Georide API returned an error due to authentication"):
        super(GeorideAPIUnauthoriedException, self).__init__(message)


@contextmanager
def handle_georide_api_http_error():
    try:
        yield
    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        if status_code == 401:
            raise GeorideAPIUnauthoriedException()
        message = err.response.json()
        raise GeorideAPIException(message)


georide_exceptions = (GeorideAPIException, GeorideAPIUnauthoriedException)
