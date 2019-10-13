from django.urls import path

from . import views

urlpatterns = [
    # path("<username>", views.road_trip, name="road-trip"),
    path("createAccountForm", views.createAccountForm, name="createAccountForm"),
    path("createAccount", views.createAccount, name="createAccount"),
    path("connectAccountForm", views.connectAccountForm, name="connectAccountForm"),
    path("connectAccount", views.connectAccount, name="connectAccount"),
    path("getInfo", views.getInfo, name="getInfo"),
    path("getToken", views.getToken, name="getToken"),
    path("getTrackers", views.getTrackers, name="getTrackers"),
    # path("positions", views.getPositions, name="positions"),
]
