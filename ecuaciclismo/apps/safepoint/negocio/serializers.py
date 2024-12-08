from collections import OrderedDict

from rest_framework import serializers, status, validators, exceptions
from django.db.models import Q

from ecuaciclismo.apps.backend.lugar.models import Local, Servicio
from ecuaciclismo.apps.backend.solicitud.models import SolicitudLugar
from ecuaciclismo.apps.backend.ruta.models import Coordenada, Ubicacion
from ecuaciclismo.apps.backend.local_detalles.models import Producto, ServicioAdicional


class CoordenadaNegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenada
        fields = (
            'id',
            'latitud',
            'longitud'
        )

      
class UbicacionNegocioSerializer(serializers.ModelSerializer):
    coordenada_x = CoordenadaNegocioSerializer()
    coordenada_y = CoordenadaNegocioSerializer()
    
    class Meta:
        model = Ubicacion
        fields = (
            'id',
            'coordenada_x',
            'coordenada_y'
        )


class NegocioSerializer(serializers.ModelSerializer):
    ubicacion = UbicacionNegocioSerializer()
    imagen = serializers.CharField(required=False)
    descripcion = serializers.CharField(required=False)
    tiene_solicitud_pendiente = serializers.SerializerMethodField()
    
    class Meta:
        model = Local
        fields = (
            'id',
            'nombre',
            'servicio',
            'imagen',
            'hora_inicio',
            'hora_fin',
            'descripcion',
            'direccion',
            'ubicacion',
            'productos',
            'servicios_adicionales',
            'tiene_solicitud_pendiente'
        )
        
    def get_tiene_solicitud_pendiente(self, obj):
        solicitud: SolicitudLugar = SolicitudLugar.objects.filter(lugar=obj)\
            .order_by("-fecha_creacion").first()
        return solicitud.estado == "Pendiente"

    def update(self, instance, validated_data: OrderedDict):
        ubicacion_data = validated_data.pop('ubicacion')
        productos_data = validated_data.pop('tipo_productos')
        servicios_adicionales_data = validated_data.pop('servicio_detalles')
        
        negocio: Local = super().update(instance, validated_data)
        negocio.ubicacion = self._actualizar_ubicacion(negocio.ubicacion, ubicacion_data)
        negocio.productos.set(productos_data)
        negocio.servicios_adicionales.set(servicios_adicionales_data)
        
        negocio.save()
        
        return negocio
        
    def _actualizar_ubicacion(self, ubicacion: Ubicacion, data: OrderedDict):
        if not ubicacion:
            coordenada_x = Coordenada(**data['coordenada_x'])
            coordenada_x.save()
            coordenada_y = Coordenada(**data['coordenada_y'])
            coordenada_y.save()
            
            ubicacion_negocio = Ubicacion(coordenada_x=coordenada_x,coordenada_y=coordenada_y)
            ubicacion_negocio.save()
            
            return ubicacion_negocio
        
        Coordenada.objects.filter(id=ubicacion.coordenada_x.id).update(**data['coordenada_x'])
        Coordenada.objects.filter(id=ubicacion.coordenada_y.id).update(**data['coordenada_y'])            
        ubicacion.refresh_from_db()
        
        return ubicacion


class SolicitudNegocioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SolicitudLugar
        fields = "__all__"


class SolicitudNegocioCreacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SolicitudLugar
        exclude = (
            'token',
            'user'
        )
        read_only_fields = (
            'id',
            'estado',
            'motivo_rechazo',
            'path_Pdf',
            'fecha_creacion',
            'ultimo_cambio'
        )
        
    def create(self, validated_data):
        usuario = self.context.get('request').user
        
        solicitud: SolicitudLugar = self._obtener_ultima_solicitud(usuario, validated_data['lugar'])
        if solicitud:
            if solicitud.estado == "Pendiente":
                raise exceptions.APIException(
                    detail= { 'message': 'Ya existe una solicitud de verificacion para este negocio' },
                    code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            elif solicitud.estado == "Aprobada":
                raise exceptions.APIException(
                    detail= { 'message': 'Este negocio ya tiene una solicitud aprobada' },
                    code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            
        solicitud = SolicitudLugar(
            user=usuario,
            lugar=validated_data['lugar'],
            estado='Pendiente',
        )
        solicitud.save()
        return solicitud
        
    def _obtener_ultima_solicitud(self, usuario, negocio):
        return SolicitudLugar.objects\
            .filter(lugar=negocio)\
            .filter(user=usuario)\
            .order_by("-fecha_creacion")\
            .first()


class ServicioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Servicio
        fields = (
            'id',
            'nombre'
        )

class ProductosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre'
        )


class ServiciosAdicionalesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServicioAdicional
        fields = (
            'id',
            'nombre'
        )
