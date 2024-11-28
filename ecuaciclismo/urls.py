"""ecuaciclismo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include, url
from django.views.static import serve

from ecuaciclismo import views
from ecuaciclismo.apps.backend.api.api_router import *
from ecuaciclismo.apps.backend.api.api_router import router
from ecuaciclismo.apps.backend.api.usuario.views import CustomAuthToken, Logout

urlpatterns = [
    path('politica/', views.current_datetime),
    path('admin/', admin.site.urls),
    path("update_server/", views.update, name="update"),
    # url(r'^(?P<application>[a-z1234567890/_-]+)/(?P<folder>media|erplib/media)/$', mediaurl, name='mediaurl'),
    # url(r'^(?P<application>[a-z1234567890/_-]+)/(?P<folder>media|erplib/media)/(?P<path>.*)$', mediaurl, name='mediaurl'),
    # url(r'^media/$', mediaurl),
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    #api
    url('^api/', include(router)),
    url('^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^api/token-auth/', CustomAuthToken.as_view()),
    url(r'^api/logout/', Logout.as_view()),
    # url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    
    path("safepoint/", include("ecuaciclismo.apps.safepoint.urls"))
]