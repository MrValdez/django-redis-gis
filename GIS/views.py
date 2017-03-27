from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Category, Location
from .serializers import CategorySerializer, LocationSerializer
from .utils import find_locations_in_radius
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
    Given a category id, lat, long, and radius,
    return the locations within that vicinity.
    '''
    if request.method == "POST":
        params = request.POST
    elif request.method == "GET":
        params = request.query_params

    try:
        category_name = params["category"]
        origin = params["lat"], params["long"]
        lat, long = float(origin[0]), float(origin[1])
        radius = int(params["radius"])
        category = get_object_or_404(Category, name=category_name)
    except (KeyError, ValueError):
        return Response({"message": "?cat={}&long={}&lat={}&radius={} needed"})

    location_ids = find_locations_in_radius(category.name, lat, long, radius)
    locations = Location.objects.filter(id__in=location_ids)
    serializer = LocationSerializer(locations,
                                    context={'request': request}, many=True)

    return Response(serializer.data)


def generate_map_url(locations):
    map = motionless.DecoratedMap()

    for location in locations:
        lat, long = location["lat"], location["long"]
        lat, long = float(lat), float(long)
        map.add_marker(motionless.LatLonMarker(lat, long))

    return map.generate_url()


def display_locations(request):
    map_url = None

    try:
        locations = get_locations_within_radius(request).data
        if locations and "message" not in locations:
            map_url = generate_map_url(locations)
        else:
            # not enough parameters in request
            locations = []
    except KeyError:
        map_url = None

    categories = Category.objects.all().values_list("name", flat=True)
    context = {"map_url": map_url,
               "locations": locations,
               "categories": categories,
               "post": request.POST}
    return render(request, "locations.html", context)
