from django.urls import path, include

urlpatterns = [
    path('autenticacion/', include('ecuaciclismo.apps.safepoint.autenticacion.urls')),
    path('negocio/', include('ecuaciclismo.apps.safepoint.negocio.urls')),
    path('inscripcion/', include('ecuaciclismo.apps.safepoint.inscripcion.urls')),
    path('consejo/', include('ecuaciclismo.apps.safepoint.consejo.urls')) 
]
