from collections import OrderedDict

from rest_framework import serializers, status, validators, exceptions

from django.db.models import Q

from ecuaciclismo.apps.backend.lugar.models import Local
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario
from .models import UsuarioNegocio

class RegistroSerializer(serializers.ModelSerializer):
    """
    Serializador para realizar el proceso de registro.
    """
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    token_notificacion = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = UsuarioNegocio
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'password2',
            'token_notificacion'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                detail= { 
                    'password': 'Las contraseñas no coinciden',
                    'password2': 'Las contraseñas no coinciden'
                },
                code=status.HTTP_400_BAD_REQUEST
            )
        return attrs
    
    def create(self, validated_data):
        usuario = UsuarioNegocio(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email']
        )
        
        usuario.set_password(validated_data['password'])
        usuario.save()
        
        detalle: DetalleUsuario = usuario.detalles
        detalle.token_notificacion = validated_data['token_notificacion']
        detalle.save()
        
        return usuario


class LoginSerializer(serializers.Serializer):
    """
    Serializador para realizar el inicio de sesion del usuario
    """
    email_username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        usuario = self._obtener_usuario_negocio(attrs['email_username'])
        
        if not usuario or not usuario.check_password(attrs['password']):
            raise exceptions.AuthenticationFailed({ 'message': 'Las credenciales no son correctas' })
        
        attrs['usuario'] = usuario
        return attrs
    
    def _obtener_usuario_negocio(self, email_username) -> UsuarioNegocio:
        return UsuarioNegocio.objects.filter(detalleusuario__isPropietary=True)\
            .filter(Q(username=email_username) | Q(email=email_username)).first()
        
    
class LocalInfoUsuarioSerializer(serializers.ModelSerializer):
    activo = serializers.BooleanField(source='isActived')
    
    class Meta:
        model = Local
        fields = (
            'id',
            'nombre',
            'imagen',
            'activo'
        )


class UsuarioNegocioSerializer(serializers.ModelSerializer):
    negocio = LocalInfoUsuarioSerializer()
    foto = serializers.CharField(source='detalleusuario.foto')
    es_propietario = serializers.BooleanField(source='detalleusuario.isPropietary')
    tipo = serializers.CharField(source='detalleusuario.tipo')
    
    class Meta:
        model = UsuarioNegocio
        fields = (
            'id',
            'username',
            'email',
            'foto',
            'es_propietario',
            'tipo',
            'negocio',
        )