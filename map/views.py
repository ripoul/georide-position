from django.shortcuts import render
import requests
import json
import os
from datetime import date, timedelta

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getPositions(request):
    url = "https://api.georide.fr/tracker/%s/trips/positions" % (os.getenv("trackerID"))
    today = date.today().strftime("%Y%m%d")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
    fromDate = "%sT020000"%(today)
    toDate = "%sT015959"%(tomorrow)
    payload = {"from": fromDate, "to": toDate}
    requestHeaders = {"Authorization": "Bearer %s" % (os.getenv("georideToken"))}
    r = requests.get(url, params=payload, headers=requestHeaders)
    return HttpResponse(r.text, content_type="application/json")
