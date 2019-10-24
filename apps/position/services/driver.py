from .serializers import PositionSerializer, TokenSerializer, TrackSerializer
from rest_framework.response import Response
from rest_framework import status


class GeorideDriver(object):

    def __init__(self, user):
        self.user = user

    def _get_authorization_header(self):
        return {'Authorization': 'Bearer {self.user.profile.token}'}

    def get_positions(self):
        data = {
            'from': self.user.profile.startDate,
            'to': self.user.profile.endDate
        }
        serializer = PositionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        url = f'https://api.georide.fr/tracker/{self.user.profile.trackerID}/trips/positions'
        payload = {'from': serializer.validated_data['from'], 'to': serializer.validated_data['to']}
        response = requests.get(url, params=payload, headers=self._get_authorization_header())
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(
                {"error": "bad credential (change it in your profile)"}, status=response.status_code
            )
        import ipdb; ipdb.set_trace()
        return Response(response.text, content_type="application/json")

    def get_new_token(self):
        url = 'https://api.georide.fr/user/login'
        payload = {'email': self.user.email, 'password': self.user.password}
        response = requests.post(url, data=payload)
        serializer = TokenSerializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def get_trackers_id(self):
        response = requests.get(
            'https://api.georide.fr/user/trackers', headers=self._get_authorization_header()
        )
        serializer = TrackSerializer(data=response.json(), many=True)
        return serializer.data

    def revokeToken(self):
        url = 'https://api.georide.fr/user/logout'
        response = requests.post(url, headers=self._get_authorization_header())
        return response.status_code
