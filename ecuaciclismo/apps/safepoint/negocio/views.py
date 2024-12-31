from django.http import Http404
from django.db.models import Count, Q, F
from django.db.models.functions import ExtractWeekDay

from rest_framework import generics, views, exceptions, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import datetime

from ecuaciclismo.apps.safepoint.autenticacion.models import UsuarioNegocio
from ecuaciclismo.apps.backend.lugar.models import Local
from ecuaciclismo.apps.backend.local_detalles.models import EstadisticaCiclistaLocal
from ecuaciclismo.apps.backend.solicitud.models import SolicitudLugar
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario

from .serializers import *

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

class ObtenerEstadoSolicitudNegocioView(ObtenerNegocioPorUsuarioMixin, generics.RetrieveAPIView):
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

class ObtenerEstadoVisibilidadNegocio(ObtenerNegocioPorUsuarioMixin, generics.RetrieveAPIView):
    """
    Clase de vista de API que devuelve el estado actual del negocio. 
    Si está activado o no y si está verificado como local seguro
    """
    serializer_class = EstadoNegocioSerializer

# 
# API Views de ayuda
#
class ServicioLocalListaView(generics.ListAPIView):
    """
    Clase de vista de API que devuelve todos los servicios disponibles para asignarle a un local.
    """
    serializer_class = ServicioSerializer
    queryset = Servicio.objects.all()
    pagination_class = None

class ProductoListaView(generics.ListAPIView):
    """
    Clase de vista de API que devuelve todos los productos disponibles para asignarle a un local.
    """
    serializer_class = ProductosSerializer
    queryset = Producto.objects.all()
    pagination_class = None
    
class ServiciosAdicionalesListaView(generics.ListAPIView):
    """
    Clase de vista de API que devuelve todos los servicios adicionales disponibles para asignarle a un local.
    """
    serializer_class = ServiciosAdicionalesSerializer
    queryset = ServicioAdicional.objects.all()
    pagination_class = None

class EstadisticaNegocioView(ObtenerNegocioPorUsuarioMixin, views.APIView):
    """
    API view que devuelve datos relacionados a las estadisticas de un negocio
    """
    
    def get(self, request, *args, **kwargs):
        serializer = self.obtener_estadisticas()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def obtener_estadisticas(self):
        if self.request.query_params.get('tipo') == 'semana':
            resultados = self._obtener_estadisticas_semana()
            return EstadisticasNegocioDiasSerializer(resultados, many=True)
            
        resultados = self._obtener_estadisticas_mes()
        return EstadisticasNegocioMesSerializer(resultados, many=True)
    
    def _obtener_estadisticas_base(self):
        negocio = self.get_object()
        return EstadisticaCiclistaLocal.objects.all().filter(local=negocio)
    
    def _obtener_estadisticas_mes(self):
        anyo_actual = datetime.datetime.now().year
        return self._obtener_estadisticas_base()\
            .filter(fecha_creacion__year=anyo_actual)\
            .values(mes=F('fecha_creacion__month'))\
            .annotate(vistas=Count('usuario'))\
            .order_by('mes')
    
    def _obtener_estadisticas_semana(self):
        semana_actual = datetime.date.today().isocalendar()[1]
        anyo_actual = datetime.date.today().isocalendar()[0]
        
        return self._obtener_estadisticas_base()\
            .filter(fecha_creacion__week=semana_actual)\
            .filter(fecha_creacion__year=anyo_actual)\
            .annotate(dia=ExtractWeekDay('fecha_creacion'))\
            .values('dia')\
            .annotate(vistas=Count('usuario'))\
            .order_by('dia')

class ActualizarEstadisticasPorCiclistaView(generics.CreateAPIView):
    """
    API endpoint que agrega un nuevo regsitro a las estadisticas de un negocio
    """
    serializer_class = EstadisticasActualizarVistaSerializer
    
    def create(self, request, *args, **kwargs):
        super().create(request, args, kwargs)
        return Response({ "message": "Se actualizaron las estadisticas correctamente" }, status=status.HTTP_200_OK)

class RegistrarAvisosNegocioView(generics.CreateAPIView):
    """
    API endpoint que realiza el registro de los llamados al 911 o entidades de seguridad
    """
    serializer_class = AgregarRegistroAvisoNegocio
    
    def create(self, request, *args, **kwargs):
        super().create(request, args, kwargs)
        return Response({ "message": "Se creo el registro correctamente" }, status=status.HTTP_200_OK)
