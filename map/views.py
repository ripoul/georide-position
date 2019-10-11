from django.shortcuts import render
import requests
import json
from datetime import date, timedelta, datetime

# Create your views here.
from django.http import HttpResponse
from .utils import get_vars


class georide_cli:
    def getPositions(self, token, trackerID, startDate, endDate):
        url = "https://api.georide.fr/tracker/%s/trips/positions" % (trackerID)
        endDate = (
            (datetime.strptime(endDate, "%Y/%m/%d") + timedelta(days=1)).strftime(
                "%Y%m%d"
            )
        ) + "T015959"
        payload = {"from": startDate.replace("/", "") + "T020000", "to": endDate}
        requestHeaders = {"Authorization": "Bearer %s" % (token)}
        r = requests.get(url, params=payload, headers=requestHeaders)
        if r.status_code == 401:
            return HttpResponse(
                {"error": "bad credential (change it in your profile)"}, status=401
            )
        return HttpResponse(r.text, content_type="application/json")

    def getNewToken(self, user, password):
        url = "https://api.georide.fr/user/login"
        payload = {"email": user, "password": password}
        r = requests.post(url, data=payload)
        return r.json()["authToken"]
    
    def getTrackersID(self, token):
        requestHeaders = {"Authorization": "Bearer %s" % (token)}
        r = requests.get("https://api.georide.fr/user/trackers", headers=requestHeaders).json()
        print(type(r))
        ret = []
        for tracker in r:
            ret.append([tracker["trackerId"], tracker["trackerName"]])
        return ret



geo = georide_cli()

"""
def road_trip(request):
    startDate = datetime.strptime(get_vars("startDate"), "%Y/%m/%d")
    endDate = datetime.strptime(get_vars("endDate"), "%Y/%m/%d")
    param = {
        "startDate": startDate.strftime("%d/%m/%Y"),
        "endDate": endDate.strftime("%d/%m/%Y"),
    }
    return render(request, "map/road-trip.html", param)
"""

"""
def getPositions(request):
    startDate = request.GET.get("startDate", get_vars("startDate"))
    endDate = request.GET.get("endDate", get_vars("endDate"))
    sd = datetime.strptime(startDate, "%Y/%m/%d")
    ldd = datetime.strptime(get_vars("startDate"), "%Y/%m/%d")
    ed = datetime.strptime(endDate, "%Y/%m/%d")
    led = datetime.strptime(get_vars("endDate"), "%Y/%m/%d")
    if sd >= ldd and ed <= led:
        return geo.getPositions(startDate=startDate, endDate=endDate)
    return HttpResponse([], content_type="application/json")
"""


def getInfo(request):
    return render(request, "map/get-info.html", {})


def getToken(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password:
            return HttpResponse(status=400)
        token = geo.getNewToken(email, password)
        ret = {"token": token}
        return HttpResponse(json.dumps(ret), content_type="application/json")
    return HttpResponse(status=405)

def getTrackers(request):
    if request.method == "POST":
        token = request.POST.get("token")
        if not token:
            return HttpResponse(status=400)
        ret = geo.getTrackersID(token)
        return HttpResponse(json.dumps(ret), content_type="application/json")
    return HttpResponse(status=405)