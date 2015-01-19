from django.conf.urls import patterns, include, url
from api.views import store_view, api_router # Import the api_router defined above
from django.contrib import admin
 
urlpatterns = patterns(
    '', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'store-(?P<store_name>[a-zA-Z]+)', store_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
