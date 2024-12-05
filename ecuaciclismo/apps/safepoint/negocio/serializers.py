from collections import OrderedDict

from rest_framework import serializers, status, validators, exceptions
from django.db.models import Q

from ecuaciclismo.apps.backend.lugar.models import Local
from ecuaciclismo.apps.backend.solicitud.models import SolicitudLugar
from ecuaciclismo.apps.backend.ruta.models import Coordenada, Ubicacion


class CoordenadaNegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenada
        exclude = (
            'token',
        )

      
class UbicacionNegocioSerializer(serializers.ModelSerializer):
    coordenada_x = CoordenadaNegocioSerializer()
    coordenada_y = CoordenadaNegocioSerializer()
    
    class Meta:
        model = Ubicacion
        exclude = (
            'token',
        )


class NegocioSerializer(serializers.ModelSerializer):
    ubicacion = UbicacionNegocioSerializer()
    imagen = serializers.CharField(required=False)
    descripcion = serializers.CharField(required=False)
    
    class Meta:
        model = Local
        fields = (
            'id',
            'servicio',
            'imagen',
            'hora_inicio',
            'hora_fin',
            'descripcion',
            'direccion',
            'ubicacion',
            'tipo_productos',
            'servicio_detalles'
        )

    def update(self, instance, validated_data: OrderedDict):
        ubicacion_data = validated_data.pop('ubicacion')
        tipo_productos_data = validated_data.pop('tipo_productos')
        servicio_detalles_data = validated_data.pop('servicio_detalles')
        
        negocio: Local = super().update(instance, validated_data)
        negocio.ubicacion = self._actualizar_ubicacion(negocio.ubicacion, ubicacion_data)
        negocio.tipo_productos.set(tipo_productos_data)
        negocio.servicio_detalles.set(servicio_detalles_data)
        
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
