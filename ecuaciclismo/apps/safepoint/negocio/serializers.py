from rest_framework import serializers, status, validators, exceptions
from django.db.models import Q

from ecuaciclismo.apps.backend.lugar.models import Local
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
