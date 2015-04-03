from django.conf.urls import patterns, include, url
from api.views import *
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
 
urlpatterns = patterns(
    '', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'store-(?P<store_name>[a-zA-Z0-9_]+)', store_view, name="store"),
    url(r's-qr/?', qr, name="qr"),
    url(r'c-order/?', customer_order, name="c-order"),
    url(r'c-menu/?', customer_menu, name="c-menu"),
    url(r'c-prod/?', customer_product, name="c-prod"),
    url(r'c-token/?', customer_pp_token, name="c-token"),
    url(r'c-status-(?P<store_name>[a-zA-Z0-9_]+)/?', customer_order_status, name="c-status"),
    url(r'c-register/?', customer_register, name="c-register"),
    url(r'^e9b14fld.htm$', ssl_check),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)