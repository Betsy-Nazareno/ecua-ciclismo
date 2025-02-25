from rest_framework import generics, status, views

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import update_last_login
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario

from .serializers import RegistroSerializer, LoginSerializer, UsuarioNegocioSerializer
from .models import UsuarioNegocio

class ObtenerInfoUsuarioNegocioMixin:
    """
    Clase mixin que crea y obtiene el token de acceso para los usuarios.
    Con su respectiva informacion
    """
    
    def autenticar_usuario(self, usuario: UsuarioNegocio):
        token, created = Token.objects.get_or_create(user=usuario)
        primer_inicio_sesion = usuario.last_login is None
        
        update_last_login(None, usuario)
        return {
            'token': token.key,
            'usuario': UsuarioNegocioSerializer(instance=usuario).data,
            'primer_inicio_sesion': primer_inicio_sesion
        } 
    

class RegistroView(ObtenerInfoUsuarioNegocioMixin, generics.CreateAPIView):
    """
    Clase para registrar usuarios.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistroSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.autenticar_usuario(serializer.instance)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class LoginView(ObtenerInfoUsuarioNegocioMixin, generics.GenericAPIView):
    """
    Clase para inicio de sesion
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['usuario']
        data = self.autenticar_usuario(user)
        return Response(data, status=status.HTTP_200_OK)

class LogoutView(views.APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
class ObtenerTokensNotificacionAdministrador(generics.ListAPIView):
    """
    Clase de vista de API que devuelve todos los tokens de notificacion de los administradores.
    """
    
    def list(self, request, *args, **kwargs):
        tokens = DetalleUsuario.objects.filter(admin=True)\
            .filter(token_notificacion__isnull=False).values_list('token_notificacion', flat=True)
        return Response(tokens, status=status.HTTP_200_OK)
