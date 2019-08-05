from django.shortcuts import render
import requests
import json
import os

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getPositions(request):
    url = "https://api.georide.fr/tracker/%s/trips/positions" % (os.getenv("trackerID"))
    fromDate = "20190805T000000"
    toDate = "20190805T235959"
    payload = {"from": fromDate, "to": toDate}
    requestHeaders = {"Authorization": "Bearer %s" % (os.getenv("georideToken"))}
    r = requests.get(url, params=payload, headers=requestHeaders)
    return HttpResponse(r.text, content_type="application/json")
