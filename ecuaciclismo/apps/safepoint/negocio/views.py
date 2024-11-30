from rest_framework import generics, views
from rest_framework.permissions import AllowAny

from .serializers import NegocioSerializer

from ecuaciclismo.apps.safepoint.autenticacion.models import UsuarioNegocio
from ecuaciclismo.apps.backend.lugar.models import Local

class ActualizarNegocioView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = Local.objects.all()
    serializer_class = NegocioSerializer

class ObtenerEstadoNegocio(views.APIView):
    
    def get(self, request, format=None):
        usuario: UsuarioNegocio = request.user