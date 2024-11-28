from rest_framework import serializers, status, validators, exceptions
from django.db.models import Q

from ecuaciclismo.apps.backend.lugar.models import Local

class NegocioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Local
        fields = "__all__"