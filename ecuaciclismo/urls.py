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
from django.urls import path, include, re_path
from django.views.static import serve

from ecuaciclismo import views
from ecuaciclismo.apps.backend.api.api_router import router
from ecuaciclismo.apps.backend.api.usuario.views import CustomAuthToken, Logout

urlpatterns = [
    path('politica/', views.current_datetime),
    path('admin/', admin.site.urls),
    path("update_server/", views.update, name="update"),

    # API
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/token-auth/', CustomAuthToken.as_view(), name="token_auth"),
    re_path(r'^api/logout/', Logout.as_view(), name="logout"),

    # SafePoint
    path("safepoint/", include("ecuaciclismo.apps.safepoint.urls")),

    # Static files
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]