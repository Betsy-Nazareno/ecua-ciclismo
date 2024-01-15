from rest_framework.authtoken.models import Token
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ecuaciclismo.apps.backend.api.bicicleta.serializers import BicicletaSerializer
from ecuaciclismo.apps.backend.bicicleta.models import Bicicleta, ImagenBicicleta, PropietarioBicicleta
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario
from ecuaciclismo.helpers import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError
from rest_framework.permissions import IsAuthenticated

class BicicletaViewSet(viewsets.ModelViewSet):
    queryset = Bicicleta.objects.all()
    serializer_class = BicicletaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False,url_path='crear_bicicleta',methods=['post'])
    def create_bicicleta(self, request):
        transaction.set_autocommit(False)
        
        print(request.data)
        try:
            data = request.data
            bicicleta = Bicicleta()
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            bicicleta.modelo = data['modelo']
            bicicleta.marca =data['marca']
            bicicleta.modalidad = data['modalidad']
            bicicleta.n_serie =data['n_serie']
            bicicleta.factura = data['factura']
            bicicleta.color =data['color']
            bicicleta.tienda_origen =data['tienda_origen']      
            bicicleta.save()
            bicicleta.codigo = bicicleta.id
            bicicleta.save()
            usuariobici = PropietarioBicicleta()
            usuariobici.usuario = token.user
            usuariobici.bicicleta = bicicleta
            usuariobici.save()
            if data.get('multimedia'):
                print(data.get('multimedia'))
                for elemento in data['multimedia']:
                    imagen = ImagenBicicleta()
                    imagen.imagen_url = elemento['link']
                    imagen.path = elemento['path']
                    imagen.bicicleta = bicicleta
                    imagen.save()
            
            transaction.commit()
            return Response({'status': 'success', 'message': 'Bicicleta creada con éxito.'})

        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': "hola"+str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})
        
    
    
    @action(detail=False, methods=['get'], url_path='mis_bicicletas')
    def get_bicicletas_por_usuario(self, request):
        try:
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            usuario = token.user
            bicicletas_usuario = PropietarioBicicleta.objects.filter(usuario=usuario).select_related('bicicleta')
            
            bicicletas = [prop.bicicleta for prop in bicicletas_usuario]
            serializer = BicicletaSerializer(bicicletas, many=True)
            
            return Response({
                "status": "success",
                "message": "Información obtenida",
                "data": serializer.data
            })

        except Token.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Token no válido"
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            })
        
    @action(detail=False, methods=['get'], url_path='user_bicicletas')
    def get_bicicletas_por_usuario_admin(self, request):
        try:
            data = request.data
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                return jsonx({'status': 'error', 'message': 'No tiene permiso para realizar esta acción.'})
            
            usuario_token = DetalleUsuario.objects.get(token=data['token_usuario'])

            bicicletas_usuario = PropietarioBicicleta.objects.filter(usuario=usuario_token.usuario).select_related('bicicleta')
            bicicletas = [prop.bicicleta for prop in bicicletas_usuario]
            serializer = BicicletaSerializer(bicicletas, many=True)
            
            return Response({
                "status": "success",
                "message": "Información obtenida",
                "data": serializer.data
            })

        except Token.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Token no válido"
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            })
        
        
    @action(detail=True, methods=['delete'], url_path='eliminar_bicicleta')
    def eliminar_bicicleta(self, request, pk=None):
        try:
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            usuario = token.user

            # Obtener la bicicleta basándose en el ID (pk) proporcionado en la URL
            bicicleta = Bicicleta.objects.get(id=pk)

            # Verificar si el usuario actual es el propietario de la bicicleta
            propietario_bicicleta = PropietarioBicicleta.objects.filter(bicicleta=bicicleta, usuario=usuario).first()
            if not propietario_bicicleta:
                return Response({'status': 'error', 'message': 'No tienes permiso para eliminar esta bicicleta'}, status=status.HTTP_403_FORBIDDEN)

            bicicleta.delete()
            return Response({'status': 'success', 'message': 'Bicicleta eliminada con éxito'})

        except Token.DoesNotExist:
            return Response({'status': 'error', 'message': 'Token no válido'}, status=status.HTTP_401_UNAUTHORIZED)
        except Bicicleta.DoesNotExist:
            return Response({'status': 'error', 'message': 'Bicicleta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
