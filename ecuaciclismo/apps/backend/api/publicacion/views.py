from rest_framework import viewsets
from rest_framework.authtoken.admin import User
from rest_framework.decorators import action

from ecuaciclismo.apps.backend.api.publicacion.serializers import PublicacionSerializer
from ecuaciclismo.apps.backend.consejodia.models import Reaccion
from ecuaciclismo.apps.backend.publicacion.models import Publicacion, DetalleEtiquetaPublicacion, \
    DetalleArchivoPublicacion
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
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            id_user = token.user.id
            data = Publicacion.get_publicaciones()
            reacciones = Reaccion.get_all_reacciones()
            for publicacion in data:
                publicacion_get = Publicacion.objects.get(token=publicacion['token'])
                diccionario_reaccion = {}
                for reaccion in reacciones:
                    dict_detalles = {}
                    resultado = Reaccion.get_reacciones_publicaciones(publicacion_get.id, reaccion['nombre'])
                    if len(resultado) > 0:
                        listado_usuarios = list(resultado[0]['usuarios'].split(","))
                        dict_detalles['usuarios'] = listado_usuarios
                        dict_detalles['reaccion_usuario'] = str(id_user) in listado_usuarios
                        diccionario_reaccion[reaccion['nombre']] = dict_detalles
                    else:
                        dict_detalles['usuarios'] = None
                        dict_detalles['reaccion_usuario'] = False
                        diccionario_reaccion[reaccion['nombre']] = dict_detalles
                publicacion['reacciones'] = diccionario_reaccion
                publicacion['etiquetas'] = DetalleEtiquetaPublicacion.get_etiqueta_x_publicacion(publicacion['id'])
                publicacion['multimedia'] = DetalleArchivoPublicacion.get_archivo_x_publicacion(publicacion['id'])
            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
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
