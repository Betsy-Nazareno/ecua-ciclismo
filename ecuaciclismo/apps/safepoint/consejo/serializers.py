from rest_framework import serializers
from .models import Consejo, Tip

class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id', 'titulo', 'detalle', 'imagen']

class ConsejoSerializer(serializers.ModelSerializer):
    tips = TipSerializer(many=True, read_only=True)

    class Meta:
        model = Consejo
        fields = ['id', 'nombre', 'icono', 'tips']
