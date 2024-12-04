from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.static import serve

from ecuaciclismo import views
from ecuaciclismo.apps.backend.api.api_router import router
from ecuaciclismo.apps.backend.api.usuario.views import CustomAuthToken, Logout

urlpatterns = [
    path('politica/', views.current_datetime),
    path('admin/', admin.site.urls),
    path("update_server/", views.update, name="update"),
    
    # Reemplazamos las antiguas URL que usaban url() por path()
    path('api/', include(router.urls)),  # Cambiado a path()
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token-auth/', CustomAuthToken.as_view()),
    path('api/logout/', Logout.as_view()),
    
    # Si aún necesitas servir archivos estáticos/media, puedes usar algo como:
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
]
