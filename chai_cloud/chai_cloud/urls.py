from django.conf.urls import patterns, include, url
from api.views import store_view, customer_order, customer_register
from django.contrib import admin
from django.views.generic import RedirectView
 
urlpatterns = patterns(
    '', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'store-(?P<store_name>[a-zA-Z]+)', store_view),
    url(r'order/?', customer_order),
    url(r'register/?', customer_register),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
)
