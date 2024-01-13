from rest_framework import serializers
from ecuaciclismo.apps.backend.bicicleta.models import ImagenBicicleta, PropietarioBicicleta, Bicicleta

class ImagenBicicletaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.CharField(max_length=200)  

    class Meta:
        model = ImagenBicicleta
        fields = ('imagen_url',)

    def create(self, validated_data):
        imagen_url = validated_data.pop('imagen_url')
        imagen_bicicleta = ImagenBicicleta.objects.create(imagen_url=imagen_url, **validated_data)
        return imagen_bicicleta


class PropietarioBicicletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropietarioBicicleta
        fields = ('usuario',)

class BicicletaSerializer(serializers.ModelSerializer):
    imagenes = ImagenBicicletaSerializer(many=True, required=False)
    propietario = PropietarioBicicletaSerializer(required=False)

    class Meta:
        model = Bicicleta
        fields = ('id','modelo','modalidad','n_serie','tienda_origen', 'factura','color','marca', 'imagenes', 'propietario')

    def create(self, validated_data):
        imagenes_data = validated_data.pop('imagenes', [])
        propietario_data = validated_data.pop('propietario', None)

        bicicleta = Bicicleta.objects.create(**validated_data)

        for imagen_data in imagenes_data:
            ImagenBicicleta.objects.create(bicicleta=bicicleta, **imagen_data)

        if propietario_data:
            PropietarioBicicleta.objects.create(bicicleta=bicicleta, **propietario_data)

        return bicicleta
