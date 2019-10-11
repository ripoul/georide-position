from django.shortcuts import render
import requests
import json
from datetime import date, timedelta, datetime

# Create your views here.
from django.http import HttpResponse
from .utils import get_vars


class georide_cli:
    trackerID = get_vars("trackerID")
    georideToken = None
    user = get_vars("userGeoride")
    password = get_vars("passwordGeoride")

    def getPositions(
        self, startDate=get_vars("startDate"), endDate=get_vars("endDate")
    ):
        url = "https://api.georide.fr/tracker/%s/trips/positions" % (self.trackerID)
        endDate = (
            (datetime.strptime(endDate, "%Y/%m/%d") + timedelta(days=1)).strftime(
                "%Y%m%d"
            )
        ) + "T015959"
        payload = {"from": startDate.replace("/", "") + "T020000", "to": endDate}
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


geo = georide_cli()


def road_trip(request):
    startDate = datetime.strptime(get_vars("startDate"), "%Y/%m/%d")
    endDate = datetime.strptime(get_vars("endDate"), "%Y/%m/%d")
    param = {
        "startDate": startDate.strftime("%d/%m/%Y"),
        "endDate": endDate.strftime("%d/%m/%Y"),
    }
    return render(request, "map/road-trip.html", param)


def getPositions(request):
    startDate = request.GET.get("startDate", get_vars("startDate"))
    endDate = request.GET.get("endDate", get_vars("endDate"))
    sd = datetime.strptime(startDate, "%Y/%m/%d")
    ldd = datetime.strptime(get_vars("startDate"), "%Y/%m/%d")
    ed = datetime.strptime(endDate, "%Y/%m/%d")
    led = datetime.strptime(get_vars("endDate"), "%Y/%m/%d")
    if sd >= ldd and ed <= led:
        ret = geo.getPositions(startDate=startDate, endDate=endDate)
        return HttpResponse(ret, content_type="application/json")
    return HttpResponse([], content_type="application/json")
