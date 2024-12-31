from rest_framework import generics
from .models import ReservaRuta
from .serializers import ReservaRutaSerializer

class ReservaRutaCreateView(generics.CreateAPIView):
    queryset = ReservaRuta.objects.all()
    serializer_class = ReservaRutaSerializer

class ReservaRutaListView(generics.ListAPIView):
    queryset = ReservaRuta.objects.all()
    serializer_class = ReservaRutaSerializer
