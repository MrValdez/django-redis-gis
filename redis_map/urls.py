from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from GIS import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'location', views.LocationViewset)

urlpatterns = [
    url(r'^$', views.index),
    url(r'^map/(?P<location_id>[0-9]+)$', views.display_map, name="display_map"),
    url(r'^locations/$', views.display_locations, name="display_locations"),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/locations', views.get_locations),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]