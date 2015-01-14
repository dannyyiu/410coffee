from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

# login imports
from django.conf.urls import include

urlpatterns = [
    ## api_view decorator method
    #url(r'^api/$', views.api_list),
    #url(r'^api/(?P<pk>[0-9]+)/$', views.api_detail),

    # APIView class method
    url(r'^api$', views.APIList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)$', views.APIDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

# format .json, .yaml url suffixes
urlpatterns = format_suffix_patterns(urlpatterns) 

# user login
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', 
                               namespace='rest_framework')),
]