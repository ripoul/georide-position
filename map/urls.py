from django.urls import path

from . import views

urlpatterns = [
    path("create", views.createAccountForm, name="createAccountForm"),
    path("createAccount", views.createAccount, name="createAccount"),
    path("connect", views.connectAccountForm, name="connectAccountForm"),
    path("connectAccount", views.connectAccount, name="connectAccount"),
    path("modify", views.modifyAccountForm, name="modifyAccountForm"),
    path("modifyAccount", views.modifyAccount, name="modifyAccount"),
    path("disconect", views.disconect, name="disconect"),
    path("getInfo", views.getInfo, name="getInfo"),
    path("getToken", views.getToken, name="getToken"),
    path("getTrackers", views.getTrackers, name="getTrackers"),
    path("positions/<username>", views.getPositions, name="positions"),
    path("trip/<username>", views.road_trip, name="road-trip"),
    path("index.html", views.index, name="index"),
    path("", views.index, name="index"),
]
