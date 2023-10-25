from django.shortcuts import render
from django.views import generic
from .models import LocationData

# Create your views here.
"""class MapView(generic.DetailView):
    model = LocationData
    template_name = "/testpage.html"
"""

def mapindex(request):
    lat = 37.541
    longi = 126.986
    mark_list = LocationData.objects.all()
    context = {
        "latitude":lat,
        "longitude":longi,
        "mark_list":mark_list,
        }
    return render(request, "testpage.html", context)