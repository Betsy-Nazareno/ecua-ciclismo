from rest_framework import serializers

from ecuaciclismo.apps.backend.ruta.models import Ruta

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'
