from rest_framework import serializers

from ecuaciclismo.apps.backend.alerta.models import Alerta

class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = '__all__'