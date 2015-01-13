from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    ## api_view decorator method
    #url(r'^api/$', views.api_list),
    #url(r'^api/(?P<pk>[0-9]+)/$', views.api_detail),

    # APIView class method
    url(r'^api/$', views.APIList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.APIDetail.as_view()),
]

# format .json, .yaml url suffixes
urlpatterns = format_suffix_patterns(urlpatterns) 