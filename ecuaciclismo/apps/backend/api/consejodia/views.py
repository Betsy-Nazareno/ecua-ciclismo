from datetime import datetime

from rest_framework import viewsets
from rest_framework.authtoken.admin import User
from rest_framework.decorators import action

from ecuaciclismo.apps.backend.api.consejodia.serializers import ConsejoDiaSerializer
from ecuaciclismo.apps.backend.consejodia.models import ConsejoDia, Novedad, Reaccion, DetalleReaccionConsejo
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none
from rest_framework import permissions



class ConsejoDiaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsejoDiaSerializer
    queryset = ConsejoDia.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(detail=False, url_path='get_consejos_dia', methods=['get'])
    def get_consejos_dia(self, request):
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            id_user = token.user.id
            data = ConsejoDia.get_consejos_del_dia()
            reacciones = Reaccion.get_all_reacciones()
            for consejo in data:
                consejo_dia = ConsejoDia.objects.get(token=consejo['token'])
                diccionario_reaccion = {}
                for reaccion in reacciones:
                    dict_detalles = {}
                    resultado = Reaccion.get_reacciones(consejo_dia.id, reaccion['nombre'])
                    if len(resultado) > 0:
                        listado_usuarios = list(resultado[0]['usuarios'].split(","))
                        dict_detalles['usuarios'] = listado_usuarios
                        dict_detalles['reaccion_usuario'] = str(id_user) in listado_usuarios
                        diccionario_reaccion[reaccion['nombre']] = dict_detalles
                    else:
                        dict_detalles['usuarios'] = None
                        dict_detalles['reaccion_usuario'] = False
                        diccionario_reaccion[reaccion['nombre']] = dict_detalles
                consejo['reacciones'] = diccionario_reaccion
            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_historico_consejos_dia', methods=['get'])
    def get_historico_consejos_dia(self, request):
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            id_user = token.user.id
            data = ConsejoDia.get_historico_consejos_del_dia()
            reacciones = Reaccion.get_all_reacciones()
            for consejo in data:
                consejo_dia = ConsejoDia.objects.get(token=consejo['token'])
                diccionario_reaccion = {}
                for reaccion in reacciones:
                    dict_detalles = {}
                    resultado = Reaccion.get_reacciones(consejo_dia.id, reaccion['nombre'])
                    if len(resultado) > 0:
                        listado_usuarios = list(resultado[0]['usuarios'].split(","))
                        dict_detalles['usuarios'] = listado_usuarios
                        dict_detalles['reaccion_usuario'] = str(id_user) in listado_usuarios
                        diccionario_reaccion[reaccion['nombre']] = dict_detalles
                    else:
                        dict_detalles['usuarios'] = None
                        dict_detalles['reaccion_usuario'] = False
                        diccionario_reaccion[reaccion['nombre']] = dict_detalles
                consejo['reacciones'] = diccionario_reaccion
            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='new_consejo_dia', methods=['post'])
    def new_consejo_dia(self, request):
        try:
            data = request.data
            consejo_dia = ConsejoDia()
            consejo_dia.informacion = data['informacion']
            consejo_dia.imagen = data['imagen']
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            consejo_dia.user = token.user
            consejo_dia.save()

            return jsonx({'status': 'success', 'message': 'Consejo del día guardado con éxito.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='update_consejo_dia', methods=['post'])
    def update_consejo_dia(self, request):
        try:
            data = request.data
            if data['token'] is not None and data['token'] != '':
                consejo_dia = ConsejoDia.objects.get(token=data['token'])
                consejo_dia.informacion = data['informacion']
                consejo_dia.imagen = data['imagen']  # GESTIONAR CON API
                from rest_framework.authtoken.models import Token
                token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
                consejo_dia.user = token.user
                consejo_dia.save()
                return jsonx({'status': 'success', 'message': 'Consejo del día actualizado con éxito.'})
            else:
                return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='delete_consejo_dia', methods=['delete'])
    def delete_consejo_dia(self, request):
        try:
            data = request.data
            if data['token'] is not None and data['token'] != '':
                consejo_dia = ConsejoDia.objects.get(token=data['token'])
                detalles_reaccion = DetalleReaccionConsejo.objects.filter(consejo_dia=consejo_dia)
                for detalle_reaccion in detalles_reaccion:
                    detalle_reaccion.delete()
                consejo_dia.delete()
                return jsonx({'status': 'success', 'message': 'Consejo del día eliminado con éxito.'})
            else:
                return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='republicar_consejo_dia', methods=['post'])
    def republicar_consejo_dia(self, request):
        try:
            data = request.data
            if data['token'] is not None and data['token'] != '':
                consejo_dia = ConsejoDia.objects.get(token=data['token'])
                consejo_dia.ultimo_cambio = datetime.now()
                consejo_dia.save()
                return jsonx({'status': 'success', 'message': 'Consejo del día republicado con éxito.'})
            else:
                return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_novedades', methods=['get'])
    def get_novedades(self, request):
        try:
            data = Novedad.get_novedades()

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='new_novedad', methods=['post'])
    def new_novedad(self, request):
        try:
            data = request.data
            novedad = Novedad()
            novedad.titulo = data['titulo']
            novedad.descripcion = data['descripcion']
            novedad.descripcion_corta = data['descripcion_corta']
            novedad.imagen = data['imagen']
            if request.data.get('nombre'):
                novedad.nombre = data['nombre']
            if request.data.get('celular'):
                novedad.celular = data['celular']
            if request.data.get('direccion'):
                novedad.direccion = data['direccion']
            novedad.save()

            return jsonx({'status': 'success', 'message': 'Novedad guardada con éxito.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='update_novedad', methods=['post'])
    def update_novedad(self, request):
        try:
            data = request.data
            if data['token'] is not None and data['token'] != '':
                novedad = Novedad.objects.get(token=data['token'])
                novedad.titulo = data['titulo']
                novedad.descripcion = data['descripcion']
                novedad.descripcion_corta = data['descripcion_corta']
                novedad.imagen = data['imagen']
                if request.data.get('nombre'):
                    novedad.nombre = data['nombre']
                if request.data.get('celular'):
                    novedad.celular = data['celular']
                if request.data.get('direccion'):
                    novedad.direccion = data['direccion']
                novedad.save()
                return jsonx({'status': 'success', 'message': 'Novedad actualizada con éxito.'})
            else:
                return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='delete_novedad', methods=['delete'])
    def delete_novedad(self, request):
        try:
            data = request.data
            if data['token'] is not None and data['token'] != '':
                novedad = Novedad.objects.get(token=data['token'])
                novedad.delete()
                return jsonx({'status': 'success', 'message': 'Novedad eliminada con éxito.'})
            else:
                return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    #REACCIONES
    @action(detail=False, url_path='post_reaccion', methods=['post'])
    def post_reaccion(self, request):
        try:
            data = request.data
            reaccion_consejo = DetalleReaccionConsejo()
            consejo_dia = ConsejoDia.objects.get(token=data['token_consejo'])
            reaccion_consejo.consejo_dia = consejo_dia
            reaccion = Reaccion.objects.get(nombre=data['nombre_reaccion'])
            reaccion_consejo.reaccion = reaccion
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            reaccion_consejo.user = token.user
            reaccion_consejo.save()

            return jsonx({'status': 'success', 'message': 'Se ha registrado la reacción con éxito.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='delete_detalle_reaccion_consejo', methods=['delete'])
    def delete_detalle_reaccion_consejo(self, request):
        try:
            data = request.data
            consejo_dia = ConsejoDia.objects.get(token=data['token_consejo'])
            reaccion = Reaccion.objects.get(nombre=data['nombre_reaccion'])
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            reaccion_consejo = DetalleReaccionConsejo.objects.get(consejo_dia=consejo_dia, reaccion=reaccion, user=token.user)
            reaccion_consejo.delete()

            return jsonx({'status': 'success', 'message': 'Se ha eliminado la reacción con éxito.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})