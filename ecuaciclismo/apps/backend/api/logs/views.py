from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from .serializers import LogSerializer
from ecuaciclismo.apps.backend.logs.models import Log

class CrearLogView(viewsets.ModelViewSet):
    serializer_class = LogSerializer
    queryset = Log.objects.all()

    @action(detail=False, url_path='crear_log', methods=['post'])
    def post(self, request):
        try:
            # Obtener el token de autorización del encabezado
            authorization_header = request.headers.get('Authorization')
            if not authorization_header or not authorization_header.startswith('Token '):
                return Response({'error': 'Token de autorización no válido'}, status=status.HTTP_401_UNAUTHORIZED)

            token_key = authorization_header.split('Token ')[1]
            token = Token.objects.get(key=token_key)

            # Obtener el usuario asociado al token
            usuario = token.user if token else None
            if not usuario:
                return Response({'error': 'Token de autorización inválido'}, status=status.HTTP_401_UNAUTHORIZED)

            # Obtener datos del cuerpo de la solicitud
            data = request.data
            uuid_log = data.get('uuidLog')
            tipo_evento = data.get('tipoEvento')
            descripcion_evento = data.get('descripcion')

            # Crear el registro de log
            nuevo_log = Log(
                uuidLog=uuid_log,
                usuario=usuario,
                tipo_evento=tipo_evento,
                descripcion_evento=descripcion_evento
            )
            nuevo_log.save()

            return Response({'message': 'Registro de log creado correctamente'}, status=status.HTTP_201_CREATED)
        
        except Token.DoesNotExist:
            return Response({'error': 'Token de autorización no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)