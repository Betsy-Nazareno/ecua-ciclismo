from rest_framework import serializers

from ecuaciclismo.apps.backend.publicacion.models import Publicacion

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'