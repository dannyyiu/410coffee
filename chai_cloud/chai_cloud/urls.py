from django.conf.urls import patterns, include, url
from api.views import *
from django.contrib import admin
from django.views.generic import RedirectView
 
urlpatterns = patterns(
    '', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'store-(?P<store_name>[a-zA-Z]+)', store_view),
    url(r's-qr/?', qr),
    url(r'c-order/?', customer_order),
    url(r'c-order/?', customer_order),
    url(r'c-menu/?', customer_menu),
    url(r'c-prod/?', customer_product),
    url(r'c-register/?', customer_register),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
)
