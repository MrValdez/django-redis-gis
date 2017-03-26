from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Category, Location
from .serializers import CategorySerializer, LocationSerializer
from .utils import find_location_in_radius
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import motionless

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LocationViewset(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_fields = ('category', 'name', 'long', 'lat')


def index(request):
    return render(request, "index.html", {})


def display_map(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    lat, long = location.lat, location.long
    lat, long = float(lat), float(long)
    map_url = motionless.CenterMap(lat=lat, lon=long).generate_url()

    context = {"lat": lat, "long": long, "map_url": map_url}
    return render(request, "map.html", context)


@api_view(["GET", "POST"])
def get_locations_within_radius(request):
    '''
    Given a lat, long, and radius, return the locations within that vicinity.
    '''
    if request.method == "POST":
        params = request.POST
    elif request.method == "GET":
        params = request.query_params

    try:
        origin = params["long"], params["lat"]
        lat, long = float(origin[0]), float(origin[1])
        radius = int(params["radius"])
    except (KeyError, ValueError):
        return Response({"message": "?long={}&lat={}&radius={} needed"})

    location_ids = find_location_in_radius(lat, long, radius)
    locations = Location.objects.filter(id__in=location_ids)
    serializer = LocationSerializer(locations, context={'request': request}, many=True)

    return Response(serializer.data)


def display_locations(request):
    map = motionless.DecoratedMap()

    try:
        locations = get_locations_within_radius(request)
        for location in locations.data:
            lat, long = location["lat"], location["long"]
            lat, long = float(lat), float(long)
            map.add_marker(motionless.LatLonMarker(lat, long))
        map_url = map.generate_url()
    except (KeyError, TypeError):
        map_url = None

    context = {"map_url": map_url, "post": request.POST}
    return render(request, "locations.html", context)