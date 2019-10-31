from django.shortcuts import render, redirect
import requests
import json
from datetime import date, timedelta, datetime
from .models import Profile
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse
from .utils import get_vars
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


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


@require_http_methods(["GET"])
def index(request):
    profiles = Profile.objects.filter
    param = {"connected": request.user.is_authenticated, "profiles": profiles}
    return render(request, "map/index.html", param)


@require_http_methods(["GET"])
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


@require_http_methods(["GET"])
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


@require_http_methods(["GET"])
def getInfo(request):
    param = {"connected": request.user.is_authenticated}
    return render(request, "map/get-info.html", param)


@require_http_methods(["POST"])
def getToken(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    if not email or not password:
        return HttpResponse(status=400)
    token = geo.getNewToken(email, password)
    ret = {"token": token}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@require_http_methods(["POST"])
def getTrackers(request):
    token = request.POST.get("token")
    if not token:
        return HttpResponse(status=400)
    ret = geo.getTrackersID(token)
    return HttpResponse(json.dumps(ret), content_type="application/json")


@require_http_methods(["GET"])
def createAccountForm(request):
    if request.user.is_authenticated:
        return redirect(reverse(road_trip, args=[request.user.username]))
    return render(request, "map/create-account.html", {})


@require_http_methods(["POST"])
def createAccount(request):
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


@require_http_methods(["GET"])
def connectAccountForm(request):
    if request.user.is_authenticated:
        return redirect(reverse(road_trip, args=[request.user.username]))
    return render(request, "map/connect-account.html", {})


@login_required
@require_http_methods(["GET"])
def disconect(request):
    username = request.user.username
    logout(request)
    return redirect(reverse(road_trip, args=[username]))


@require_http_methods(["POST"])
def connectAccount(request):
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


@login_required
@require_http_methods(["GET"])
def modifyAccountForm(request):
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


@login_required
@require_http_methods(["POST"])
def modifyAccount(request):
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


@login_required
@require_http_methods(["POST"])
def revokeToken(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    token = profile.token
    return HttpResponse(status=geo.revokeToken(token))


@login_required
@require_http_methods(["POST"])
def deleteUser(request):
    user = request.user
    user.delete()
    return redirect(reverse(index))
