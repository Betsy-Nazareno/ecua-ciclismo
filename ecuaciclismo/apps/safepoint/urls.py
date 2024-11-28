from django.urls import path, include

urlpatterns = [
    path('autenticacion/', include('ecuaciclismo.apps.safepoint.autenticacion.urls'))
]
