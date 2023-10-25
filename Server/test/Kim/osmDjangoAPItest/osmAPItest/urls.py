from django.urls import path
from . import views

urlpatterns = [
    path("", views.mapindex, name="mapindex"),
]