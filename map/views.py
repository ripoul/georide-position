from django.shortcuts import render
import requests
import json
from datetime import date, timedelta

# Create your views here.
from django.http import HttpResponse
from .utils import get_vars


class georide_cli:
    trackerID = get_vars("trackerID")
    georideToken = None
    user = get_vars("userGeoride")
    password = get_vars("passwordGeoride")

    def getPositions(self):
        url = "https://api.georide.fr/tracker/%s/trips/positions" % (self.trackerID)
        today = date.today().strftime("%Y%m%d")
        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
        fromDate = "%sT020000" % (today)
        toDate = "%sT015959" % (tomorrow)
        payload = {"from": fromDate, "to": toDate}
        requestHeaders = {"Authorization": "Bearer %s" % (self.georideToken)}
        r = requests.get(url, params=payload, headers=requestHeaders)
        if r.status_code == 401:
            self.getNewToken()
            requestHeaders = {"Authorization": "Bearer %s" % (self.georideToken)}
            r = requests.get(url, params=payload, headers=requestHeaders)
        return r.text

    def getNewToken(self):
        url = "https://api.georide.fr/user/login"
        payload = {"email": self.user, "password": self.password}
        r = requests.post(url, data=payload)
        self.georideToken = r.json()["authToken"]


def index(request):
    return render(request, "map/index.html", {})


def getPositions(request):
    georide = georide_cli()
    ret = georide.getPositions()
    return HttpResponse(ret, content_type="application/json")
