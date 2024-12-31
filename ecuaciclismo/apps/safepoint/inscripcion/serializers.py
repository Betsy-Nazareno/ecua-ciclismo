from rest_framework import serializers
from .models import ReservaRuta

class ReservaRutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaRuta
        fields = '__all__'
