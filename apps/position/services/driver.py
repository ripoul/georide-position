import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from .exceptions import handle_georide_api_http_error
from .serializers import PositionSerializer, TokenSerializer, TrackSerializer


class GeorideDriver(object):
    def _get_token_cache_key(self, email, password):
        return f"{email}_{password}_georide_token"

    def _get_token_from_cache(self, email, password):
        cache_key = self._get_token_cache_key(email, password)
        cached_token = cache.get(cache_key)
        if cached_token:
            return cached_token

    def _set_token_in_cache(self, email, password, token):
        cache_key = self._get_token_cache_key(email, password)
        cache.set(cache_key, token)

    def _remove_token_from_cache(self, email, password):
        cache_key = self._get_token_cache_key(email, password)
        cache.delete(cache_key)


class GeorideAnonymousDriver(GeorideDriver):
    def _get_authorization_header(self, token):
        return {"Authorization": f"Bearer {token}"}

    def get_positions(self, token):
        data = {"from": self.user.profile.startDate, "to": self.user.profile.endDate}
        serializer = PositionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        url = f"https://api.georide.fr/tracker/{self.user.profile.trackerID}/trips/positions"
        payload = {
            "from": serializer.validated_data["from"],
            "to": serializer.validated_data["to"],
        }
        response = requests.get(
            url, params=payload, headers=self._get_authorization_header(token)
        )
        with handle_georide_api_http_error():
            response.raise_for_status()
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(
                {"error": "bad credential (change it in your profile)"},
                status=response.status_code,
            )
        return Response(response.text, content_type="application/json")

    def get_new_token(self, email, password):
        cached_token = self._get_token_from_cache(email, password)
        if cached_token:
            return cached_token
        else:
            url = "https://api.georide.fr/user/login"
            payload = {"email": email, "password": password}
            response = requests.post(url, data=payload)
            with handle_georide_api_http_error():
                response.raise_for_status()
            serializer = TokenSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)
            token = serializer.data["authToken"]
            self._set_token_in_cache(email, password, token)
            return token

    def get_trackers_id(self, token):
        response = requests.get(
            "https://api.georide.fr/user/trackers",
            headers=self._get_authorization_header(token),
        )
        with handle_georide_api_http_error():
            response.raise_for_status()
        serializer = TrackSerializer(data=response.json(), many=True)
        serializer.is_valid(raise_exception=True)
        tracker_list = [
            ([tracker["trackerId"], tracker["trackerName"]])
            for tracker in serializer.data
        ]
        return tracker_list

    def revoke_token(self, token, email, password):
        url = "https://api.georide.fr/user/logout"
        response = requests.post(url, headers=self._get_authorization_header(token))
        with handle_georide_api_http_error():
            response.raise_for_status()
        self._remove_token_from_cache(email, password)
        return response.status_code


georide_anonymous_driver = GeorideAnonymousDriver()


class GeorideDriverAuthenticated(GeorideDriver):
    def __init__(self, user):
        self.user = user

    def _get_authorization_header(self):
        return {"Authorization": f"Bearer {self.user.token}"}

    def get_positions(self):
        data = {"from": self.user.profile.start_date, "to": self.user.profile.end_date}
        serializer = PositionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        url = f"https://api.georide.fr/tracker/{self.user.profile.tracker_id}/trips/positions"
        payload = {
            "from": serializer.validated_data["from"],
            "to": serializer.validated_data["to"],
        }
        response = requests.get(
            url, params=payload, headers=self._get_authorization_header()
        )
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(
                {"error": "bad credential (change it in your profile)"},
                status=response.status_code,
            )
        return Response(response.text, content_type="application/json")

    def get_new_token(self):
        cached_token = self._get_token_from_cache(self.user.email, self.user.password)
        if cached_token:
            token = cached_token
        else:
            url = "https://api.georide.fr/user/login"
            payload = {"email": self.user.email, "password": self.user.password}
            response = requests.post(url, data=payload)
            with handle_georide_api_http_error():
                response.raise_for_status()
            serializer = TokenSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)
            token = serializer.data["authToken"]
            self._set_token_in_cache(self.user.email, self.user.password, token)
        self.user.token = token
        self.user.save()
        return token

    def get_trackers_id(self):
        response = requests.get(
            "https://api.georide.fr/user/trackers",
            headers=self._get_authorization_header(),
        )
        with handle_georide_api_http_error():
            response.raise_for_status()
        serializer = TrackSerializer(data=response.json(), many=True)
        serializer.is_valid(raise_exception=True)
        # TODO: Edit profile model to a one many to user and register every trackers
        tracker_list = [
            ([tracker["trackerId"], tracker["trackerName"]])
            for tracker in serializer.data
        ]
        return tracker_list

    def revoke_token(self):
        url = "https://api.georide.fr/user/logout"
        response = requests.post(url, headers=self._get_authorization_header())
        with handle_georide_api_http_error():
            response.raise_for_status()
        self.user.token = None
        self.user.save()
        self._remove_token_from_cache(self.user.email, self.user.password)
        return response.status_code
