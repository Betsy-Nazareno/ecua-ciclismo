from django.urls import path

from . import views

urlpatterns = [
    path('obtener_actualizar', views.ObtenerDetalleActualizarNegocioView.as_view(), name='obtener_actualizar_negocio'),
    path('obtener_solicitud', views.ObtenerEstadoNegocioView.as_view(), name='solicitud_negocio'),
    path('generar_solicitud', views.CrearSolicitudNegocioView.as_view(), name='generar_solicitud'),
    
    path('productos', views.ProductoListaView.as_view(), name='listado_productos_local'),    
    path('servicios', views.ServicioLocalListaView.as_view(), name='listado_servicios'),
    path('servicios_adicionales', views.ServiciosAdicionalesListaView.as_view(), name='listado_servicios_adicionales_local'),
    
    path('actualizar/<int:pk>', views.UpdateNegocioView.as_view(), name='obtener_actualizar_negocio'),    
]
