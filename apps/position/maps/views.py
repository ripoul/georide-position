import json
from datetime import date, datetime, timedelta

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from position.accounts.models import Profile

from .utils import get_vars


class georide_cli:
    def getPositions(self, token, trackerID, startDate, endDate):
        url = "https://api.georide.fr/tracker/%s/trips/positions" % (trackerID)
        endDate = ((endDate + timedelta(days=1)).strftime("%Y%m%d")) + "T015959"
        payload = {"from": startDate.strftime("%Y%m%d") + "T020000", "to": endDate}
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
        r = requests.get(
            "https://api.georide.fr/user/trackers", headers=requestHeaders
        ).json()
        ret = []
        for tracker in r:
            ret.append([tracker["trackerId"], tracker["trackerName"]])
        return ret

    def revokeToken(self, token):
        url = "https://api.georide.fr/user/logout"
        requestHeaders = {"Authorization": "Bearer %s" % (token)}
        r = requests.post(url, headers=requestHeaders)
        return r.status_code


geo = georide_cli()


def index(request):
    profiles = Profile.objects.filter
    param = {"connected": request.user.is_authenticated, "profiles": profiles}
    return render(request, "map/index.html", param)


def road_trip(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    param = {
        "username": username,
        "startDate": profile.startDate.strftime("%d/%m/%Y"),
        "endDate": profile.endDate.strftime("%d/%m/%Y"),
        "connected": request.user.is_authenticated,
    }
    return render(request, "map/road-trip.html", param)


def getPositions(request, username):
    startDateReq = request.GET.get("startDate", None)
    endDateReq = request.GET.get("endDate", None)

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    if startDateReq is None or endDateReq is None:
        return geo.getPositions(
            profile.token, profile.trackerID, profile.startDate, profile.endDate
        )

    sd = datetime.strptime(startDateReq, "%Y/%m/%d")
    ed = datetime.strptime(endDateReq, "%Y/%m/%d")
    if sd.date() >= profile.startDate and ed.date() <= profile.endDate:
        return geo.getPositions(profile.token, profile.trackerID, sd.date(), ed.date())
    return HttpResponse([], content_type="application/json")


def getInfo(request):
    param = {"connected": request.user.is_authenticated}
    return render(request, "map/get-info.html", param)


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


def createAccountForm(request):
    if request.user.is_authenticated:
        return redirect(reverse(road_trip, args=[request.user.username]))
    return render(request, "map/create-account.html", {})


def createAccount(request):
    if request.method == "POST":
        username = request.POST.get("id")
        email = request.POST.get("email")
        token = request.POST.get("token")
        trackerID = request.POST.get("trackerID")
        password = request.POST.get("password")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        if (
            not username
            or not email
            or not token
            or not trackerID
            or not password
            or not startDate
            or not endDate
        ):
            return HttpResponse(status=400)
        trackerID = int(trackerID)
        # check date
        try:
            profile = Profile.objects.create_profile(
                username, email, password, token, trackerID, startDate, endDate
            )
            profile.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return HttpResponse(status=202)
        except IntegrityError:
            return HttpResponse(status=500)
    return HttpResponse(status=405)


def connectAccountForm(request):
    if request.user.is_authenticated:
        return redirect(reverse(road_trip, args=[request.user.username]))
    return render(request, "map/connect-account.html", {})


def disconect(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        return redirect(reverse(road_trip, args=[username]))
    return redirect(reverse(index))


def connectAccount(request):
    if request.method == "POST":
        username = request.POST.get("id")
        password = request.POST.get("password")
        if not username or not password:
            return HttpResponse(status=400)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse(status=500)
        return HttpResponse(status=202)
    return HttpResponse(status=405)


def modifyAccountForm(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        startDate = profile.startDate.strftime("%Y-%m-%d")
        endDate = profile.endDate.strftime("%Y-%m-%d")
        param = {
            "id": user.username,
            "email": user.email,
            "startDate": startDate,
            "endDate": endDate,
            "token": profile.token,
            "trackerID": profile.trackerID,
            "connected": request.user.is_authenticated,
        }
        return render(request, "map/modify-account.html", param)
    return redirect(reverse(connectAccountForm))


def modifyAccount(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.objects.get(user=user)

            username = request.POST.get("id")
            email = request.POST.get("email")
            token = request.POST.get("token")
            trackerID = request.POST.get("trackerID")
            startDate = request.POST.get("startDate")
            endDate = request.POST.get("endDate")

            if (
                not username
                or not email
                or not token
                or not trackerID
                or not startDate
                or not endDate
            ):
                return HttpResponse(status=400)

            user.username = username
            user.email = email
            user.save()

            profile.token = token
            profile.trackerID = trackerID
            profile.startDate = startDate
            profile.endDate = endDate
            profile.save()
            return HttpResponse(status=202)
        return HttpResponse(status=403)
    return HttpResponse(status=405)


def revokeToken(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.objects.get(user=user)
            token = profile.token
            return HttpResponse(status=geo.revokeToken(token))
        return HttpResponse(status=403)
    return HttpResponse(status=405)
