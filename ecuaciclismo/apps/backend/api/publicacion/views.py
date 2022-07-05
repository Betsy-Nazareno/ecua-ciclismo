from rest_framework import viewsets
from rest_framework.authtoken.admin import User
from rest_framework.decorators import action

from ecuaciclismo.apps.backend.api.publicacion.serializers import PublicacionSerializer
from ecuaciclismo.apps.backend.publicacion.models import Publicacion, DetalleEtiquetaPublicacion
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none
from rest_framework import permissions



class PublicacionViewSet(viewsets.ModelViewSet):
    serializer_class = PublicacionSerializer
    queryset = Publicacion.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(detail=False, url_path='get_publicaciones', methods=['get'])
    def get_publicaciones(self, request):
        try:
            data = Publicacion.get_publicaciones()
            for d in data:
                print(d['id']) #REMOVER ID
                d['etiquetas'] = DetalleEtiquetaPublicacion.get_etiqueta_x_publicacion(d['id'])
            print(data)

            return jsonx({'status':'success', 'message':'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status':'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    # @action(detail=False, url_path='new_consejo_dia', methods=['post'])
    # def new_consejo_dia(self, request):
    #     try:
    #         data = request.data
    #         consejo_dia = ConsejoDia()
    #         consejo_dia.informacion = data['informacion']
    #         consejo_dia.imagen = data['imagen']
    #         from rest_framework.authtoken.models import Token
    #         token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
    #         consejo_dia.user = token.user
    #         consejo_dia.save()
    #
    #         return jsonx({'status': 'success', 'message': 'Consejo del día guardado con éxito.'})
    #     except ApplicationError as msg:
    #         return jsonx({'status': 'error', 'message': str(msg)})
    #     except Exception as e:
    #         return jsonx({'status': 'error', 'message': str(e)})

    # @action(detail=False, url_path='update_consejo_dia', methods=['post'])
    # def update_consejo_dia(self, request):
    #     try:
    #         data = request.data
    #         if data['token'] is not None and data['token'] != '':
    #             consejo_dia = ConsejoDia.objects.get(token=data['token'])
    #             consejo_dia.informacion = data['informacion']
    #             consejo_dia.imagen = data['imagen']  # GESTIONAR CON API
    #             from rest_framework.authtoken.models import Token
    #             token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
    #             consejo_dia.user = token.user
    #             consejo_dia.save()
    #             return jsonx({'status': 'success', 'message': 'Consejo del día actualizado con éxito.'})
    #         else:
    #             return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
    #     except ApplicationError as msg:
    #         return jsonx({'status': 'error', 'message': str(msg)})
    #     except Exception as e:
    #         return jsonx({'status': 'error', 'message': str(e)})
    #
    # @action(detail=False, url_path='delete_consejo_dia', methods=['delete'])
    # def delete_consejo_dia(self, request):
    #     try:
    #         data = request.data
    #         if data['token'] is not None and data['token'] != '':
    #             consejo_dia = ConsejoDia.objects.get(token=data['token'])
    #             consejo_dia.delete()
    #             return jsonx({'status': 'success', 'message': 'Consejo del día eliminado con éxito.'})
    #         else:
    #             return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
    #     except ApplicationError as msg:
    #         return jsonx({'status': 'error', 'message': str(msg)})
    #     except Exception as e:
    #         return jsonx({'status': 'error', 'message': str(e)})