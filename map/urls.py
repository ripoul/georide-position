from django.urls import path

from . import views

urlpatterns = [
    # path("", views.road_trip, name="road-trip"),
    path("getInfo", views.getInfo, name="getInfo"),
    path("getToken", views.getToken, name="getToken"),
    path("getTrackers", views.getTrackers, name="getTrackers"),
    # path("positions", views.getPositions, name="positions"),
]
