from django.contrib.auth.models import User

from rest_framework import serializers

from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario
from ecuaciclismo.base.models import RegistroCambiarClave


class UsuarioSerializer(serializers.ModelSerializer):
    # avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # lookup_field = 'username'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'username'}
        # }
    # def get_avatar(self, obj):
    #     return settings.URL_DJANGO_SERVER + reverse(servir_imagen_perfil, args=[obj.detalleusuario.token_publico])

class DetalleUsuarioSerializer(serializers.ModelSerializer):
    # avatar = serializers.SerializerMethodField('get_avatar', read_only=True)
    correo  = serializers.SerializerMethodField('get_correo')

    class Meta:
        model = DetalleUsuario
        fields = ('token_publico', 'correo')
        lookup_field = 'token_publico'
        extra_kwargs = {
            'url': {'lookup_field': 'token_publico'}
        }

    def to_representation(self, instance):
        self.fields['usuario'] =  UsuarioSerializer(read_only=True)

        return super(DetalleUsuarioSerializer, self).to_representation(instance)

    # def get_avatar(self, obj):
    #     return settings.URL_DJANGO_SERVER + reverse(servir_imagen_perfil, args=[obj.token_publico]) + '?update=' + str(random.randint(1, 99))

    def get_correo(self, obj):
        return obj.usuario.email


class UsuarioRecuperarClaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroCambiarClave
        fields = ('token', 'usuario')
