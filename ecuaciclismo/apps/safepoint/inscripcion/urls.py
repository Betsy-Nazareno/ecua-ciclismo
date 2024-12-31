from django.urls import path
from .views import ReservaRutaCreateView,ReservaRutaListView

urlpatterns = [
    path('reservas/', ReservaRutaCreateView.as_view(), name='crear-reserva'),
    path('rutas/', ReservaRutaListView.as_view(), name='ruta-list'),
]
