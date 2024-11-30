from django.urls import path

from . import views

urlpatterns = [
    path('actualizar/<int:pk>', views.ActualizarNegocioView.as_view(), name='actualizar_negocio'),
]
