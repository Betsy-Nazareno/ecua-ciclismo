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
            'ubicacion'
        )


class SolicitudNegocioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SolicitudLugar
        fields = "__all__"


class SolicitudNegocioCreacionSerializer(serializers.ModelSerializer):
    lugar = serializers.PrimaryKeyRelatedField(required=True)
    
    class Meta:
        model = SolicitudLugar
        fields = "__all__"
        
    def create(self, validated_data):
        usuario = self.context.get('request').user
        
        solicitud: SolicitudLugar = self._obtener_ultima_solicitud(usuario, validated_data['lugar'])
        if solicitud and solicitud.estado == "Pendiente":
            return solicitud
        
        solicitud = SolicitudLugar(
            user=usuario,
            lugar__id=validated_data['lugar'],
            estado='Pendiente',
        )
        solicitud.save()
        return solicitud
        
    def _obtener_ultima_solicitud(self, usuario, negocio_id):
        return SolicitudLugar.objects\
            .filter(lugar__id=negocio_id)\
            .filter(user=usuario)\
            .filter(Q(estado='Pendiente') | Q(estado='Rechazada'))\
            .order_by("-fecha_creacion")\
            .first()
