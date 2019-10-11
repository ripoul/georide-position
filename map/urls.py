from django.urls import path

from . import views

urlpatterns = [
    path("", views.road_trip, name="road-trip"),
    path("positions", views.getPositions, name="positions"),
]
