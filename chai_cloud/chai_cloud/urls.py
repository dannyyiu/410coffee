from django.conf.urls import patterns, include, url
from api.views import api_router # Import the api_router defined above
from django.contrib import admin
 
urlpatterns = patterns(
    '', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(api_router.urls)),)
