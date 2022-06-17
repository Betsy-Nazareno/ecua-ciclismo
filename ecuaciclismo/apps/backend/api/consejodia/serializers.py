from rest_framework import serializers

from ecuaciclismo.apps.backend.consejodia.models import ConsejoDia

class ConsejoDiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsejoDia
        fields = '__all__'