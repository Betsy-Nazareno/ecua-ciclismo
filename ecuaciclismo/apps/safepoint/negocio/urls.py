from django.urls import path

from . import views

urlpatterns = [
    path('obtener_actualizar', views.ObtenerDetalleActualizarNegocioView.as_view(), name='obtener_actualizar_negocio'),
    path('obtener_solicitud', views.ObtenerEstadoNegocioView.as_view(), name='solicitud_negocio'),
    path('generar_solicitud', views.CrearSolicitudNegocioView.as_view(), name='generar_solicitud')
]
