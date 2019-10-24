import requests
from rest_framework import status
from rest_framework.response import Response

from .serializers import PositionSerializer, TokenSerializer, TrackSerializer


class GeorideUnauthenticatedDriver(object):
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
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(
                {"error": "bad credential (change it in your profile)"},
                status=response.status_code,
            )
        return Response(response.text, content_type="application/json")

    def get_new_token(self, email, password):
        url = "https://api.georide.fr/user/login"
        payload = {"email": email, "password": password}
        response = requests.post(url, data=payload)
        serializer = TokenSerializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        return serializer.data["authToken"]

    def get_trackers_id(self, token):
        response = requests.get(
            "https://api.georide.fr/user/trackers",
            headers=self._get_authorization_header(token),
        )
        serializer = TrackSerializer(data=response.json(), many=True)
        serializer.is_valid(raise_exception=True)
        tracker_list = [
            ([tracker["trackerId"], tracker["trackerName"]])
            for tracker in serializer.data
        ]
        return tracker_list

    def revoke_token(self, token):
        url = "https://api.georide.fr/user/logout"
        response = requests.post(url, headers=self._get_authorization_header(token))
        return response.status_code


georide_unauthenticated_driver = GeorideUnauthenticatedDriver()


class GeorideDriver(object):
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
        url = "https://api.georide.fr/user/login"
        payload = {"email": self.user.email, "password": self.user.password}
        response = requests.post(url, data=payload)
        serializer = TokenSerializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        self.user.token = serializer.data["authToken"]
        self.user.save()
        return serializer.data["authToken"]

    def get_trackers_id(self):
        response = requests.get(
            "https://api.georide.fr/user/trackers",
            headers=self._get_authorization_header(),
        )
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
        self.user.token = None
        self.user.save()
        return response.status_code
