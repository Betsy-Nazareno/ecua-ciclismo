from rest_framework import serializers

from ecuaciclismo.apps.backend.lugar.models import Lugar

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = '__all__'