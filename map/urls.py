from django.urls import path

from . import views

urlpatterns = [
    path("create", views.createAccountForm, name="createAccountForm"),
    path("createAccount", views.createAccount, name="createAccount"),
    path("connect", views.connectAccountForm, name="connectAccountForm"),
    path("connectAccount", views.connectAccount, name="connectAccount"),
    path("modifie", views.modifieAccountForm, name="modifieAccountForm"),
    path("modifieAccount", views.modifieAccount, name="modifieAccount"),
    path("disconect", views.disconect, name="disconect"),
    path("getInfo", views.getInfo, name="getInfo"),
    path("getToken", views.getToken, name="getToken"),
    path("getTrackers", views.getTrackers, name="getTrackers"),
    path("positions/<username>", views.getPositions, name="positions"),
    path("trip/<username>", views.road_trip, name="road-trip"),
]
