from django.http import Http404

from rest_framework import generics, views, exceptions
from rest_framework.permissions import AllowAny

from ecuaciclismo.apps.safepoint.autenticacion.models import UsuarioNegocio
from ecuaciclismo.apps.backend.lugar.models import Local
from ecuaciclismo.apps.backend.solicitud.models import SolicitudLugar
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario

from .serializers import NegocioSerializer, SolicitudNegocioSerializer, SolicitudNegocioCreacionSerializer

class ObtenerNegocioPorUsuarioMixin:
    """
    Clase mixin que obtiene el local asociado a un dueño de negocio mediante los datos del usuario autenticado 
    en la peticion mediante el token que se pasa por los headers.
    """
    
    def get_object(self) -> Local:
        usuario: UsuarioNegocio = UsuarioNegocio.objects.get(pk=self.request.user.id)
        
        detalle_usuario: DetalleUsuario = usuario.detalles        
        if not detalle_usuario.isPropietary:
            raise exceptions.NotFound(detail={ 'message': 'El usuario no es un dueño de negocio' })
        
        negocio: Local = usuario.negocio        
        if not negocio:
            raise Http404
        
        return negocio

class ObtenerDetalleActualizarNegocioView(ObtenerNegocioPorUsuarioMixin, generics.RetrieveUpdateAPIView):
    """
    Clase de vista de API que devuelve y actualiza datos de un local.
    - Metodo GET: Devuelve datos del negocio asociado al usuario
    - Metodo PUT: Actualiza los datos del negocio asociado al usuario
    """
    serializer_class = NegocioSerializer


class ObtenerEstadoNegocioView(ObtenerNegocioPorUsuarioMixin, generics.RetrieveAPIView):
    serializer_class = SolicitudNegocioSerializer
    
    def get_object(self):
        negocio: Local = super().get_object()
        return SolicitudLugar.objects.filter(lugar=negocio).filter(user=self.request.user)\
            .order_by("-fecha_creacion").first()


class CrearSolicitudNegocioView(generics.CreateAPIView):
    serializer_class = SolicitudNegocioCreacionSerializer

class UpdateNegocioView(generics.UpdateAPIView):
    serializer_class = NegocioSerializer
    queryset = Local.objects.all()
    permission_classes = (AllowAny,)
