from django.conf.urls import patterns, include, url
from api.views import store_view, customer_order
from django.contrib import admin
 
urlpatterns = patterns(
    '', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'store-(?P<store_name>[a-zA-Z]+)', store_view),
    url(r'order/', customer_order),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
)
