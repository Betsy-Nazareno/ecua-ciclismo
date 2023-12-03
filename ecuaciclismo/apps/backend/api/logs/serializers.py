from rest_framework import serializers
from ecuaciclismo.apps.backend.logs.models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'fecha', 'uuidLog', 'usuario', 'tipo_evento', 'descripcion_evento']
