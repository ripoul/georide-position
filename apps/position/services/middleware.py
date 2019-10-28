from django.http import JsonResponse
from rest_framework.exceptions import APIException

from .exceptions import georide_exceptions


class APIExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, georide_exceptions):
            return JsonResponse(
                {"data": exception.main_message}, status=exception.status
            )
        if isinstance(exception, APIException):
            # Already logged into sentry
            return JsonResponse(
                {"data": exception.detail}, status=exception.status_code
            )
        return None
