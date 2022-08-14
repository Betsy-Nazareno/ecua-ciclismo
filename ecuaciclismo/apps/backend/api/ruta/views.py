from django.db import transaction
from rest_framework import viewsets

from ecuaciclismo.apps.backend.api.ruta.serializers import RutaSerializer
from ecuaciclismo.apps.backend.ruta.models import Ruta, Coordenada, Ubicacion, Requisito, DetalleRequisito, \
    EtiquetaRuta, DetalleEtiquetaRuta, Archivo, DetalleArchivoRuta, Colaboracion, DetalleColaboracion, InscripcionRuta, \
    DetalleColaboracionInscripcion

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none


class RutaViewSet(viewsets.ModelViewSet):
    serializer_class = RutaSerializer
    queryset = Ruta.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(detail=False, url_path='new_ruta', methods=['post'])
    def new_ruta(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            ruta = Ruta()
            ruta.nombre = data['nombre']
            ruta.descripcion = data['descripcion']
            ruta.estado = 'Disponible'
            if data.get('cupos_disponibles'):
                ruta.cupos_disponibles = data['cupos_disponibles']
            ruta.lugar = data['lugar']
            ruta.fecha_inicio = data['fecha_inicio']
            ruta.fecha_fin = data['fecha_fin']
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                ruta.aprobado = 0
            else:
                ruta.aprobado = 1
            ruta.user = token.user
            coordenadax = Coordenada.objects.create(latitud=data['ubicacion']['coordinateX']['latitude'],longitud=data['ubicacion']['coordinateX']['longitude'])
            coordenaday = Coordenada.objects.create(latitud=data['ubicacion']['coordinateY']['latitude'],longitud=data['ubicacion']['coordinateY']['longitude'])
            ubicacion = Ubicacion.objects.create(coordenada_x=coordenadax, coordenada_y=coordenaday)
            ruta.ubicacion = ubicacion
            ruta.save()

            if data.get('requisitos'):
                for requisito_token in data['requisitos']:
                    requisito_save = get_or_none(Requisito, token=requisito_token)
                    if requisito_save is not None:
                        detalle_requisito = DetalleRequisito()
                        detalle_requisito.requisito = requisito_save
                        detalle_requisito.ruta = ruta
                        detalle_requisito.save()

            if data.get('colaboraciones'):
                for colaboracion_token in data['colaboraciones']:
                    colaboracion_save = get_or_none(Colaboracion, token=colaboracion_token)
                    if colaboracion_save is not None:
                        detalle_colaboracion = DetalleColaboracion()
                        detalle_colaboracion.colaboracion = colaboracion_save
                        detalle_colaboracion.ruta = ruta
                        detalle_colaboracion.save()

            if data.get('tipoRuta'):
                for token_tipo_ruta in data['tipoRuta']:
                    etiqueta_ruta = get_or_none(EtiquetaRuta,token=token_tipo_ruta)
                    if etiqueta_ruta is not None:
                        detalle_etiqueta_ruta = DetalleEtiquetaRuta()
                        detalle_etiqueta_ruta.ruta = ruta
                        detalle_etiqueta_ruta.etiqueta = etiqueta_ruta
                        detalle_etiqueta_ruta.save()

            if data.get('fotos'):
                for elemento in data['fotos']:
                    archivo = Archivo()
                    archivo.link = elemento['link']
                    archivo.tipo = 'imagen'
                    archivo.path = elemento['path']
                    archivo.save()
                    detalle_archivo_ruta = DetalleArchivoRuta()
                    detalle_archivo_ruta.archivo = archivo
                    detalle_archivo_ruta.ruta = ruta
                    detalle_archivo_ruta.save()

            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Ruta guardado con éxito.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_requisitos', methods=['get'])
    def get_requisitos(self, request):
        try:
            data = Requisito.get_requisitos()
            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_colaboraciones', methods=['get'])
    def get_colaboraciones(self, request):
        try:
            data = Colaboracion.get_colaboraciones()
            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_tipos_rutas', methods=['get'])
    def get_tipos_rutas(self, request):
        try:
            data = EtiquetaRuta.get_tipos_rutas()
            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_ruta', methods=['post'])
    def get_ruta(self, request):
        try:
            data_busqueda = request.data
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            data = Ruta.get_ruta(token_ruta=data_busqueda['token_ruta'])

            for ruta in data:
                if ruta['cancelada'] == 1:
                    diccionario = {'estado_cancelado': 1, 'prioridad': 4}
                    ruta['estado'] = diccionario
                elif ruta['finalizado'] == True:
                    diccionario = {'estado_finalizado': ruta['estado_finalizado'], 'prioridad': 5}
                    ruta['estado'] = diccionario
                elif ruta['estado_en_curso'] == True:
                    diccionario = {'estado_en_curso': ruta['estado_en_curso'], 'prioridad': 1}
                    ruta['estado'] = diccionario
                elif ruta['estado_finalizado'] == True:
                    diccionario = {'estado_finalizado': ruta['estado_finalizado'], 'prioridad': 5}
                    ruta['estado'] = diccionario
                elif ruta['cupos_disponibles'] is not None:
                    if ruta['cupos_disponibles'] <= 0:
                        diccionario = {'estado_sin_cupos': 1, 'prioridad': 3}
                        ruta['estado'] = diccionario
                    elif ruta['estado_no_iniciada'] == True:
                        diccionario = {'estado_no_iniciada': ruta['estado_no_iniciada'], 'prioridad': 2}
                        ruta['estado'] = diccionario
                elif ruta['estado_no_iniciada'] == True:
                    diccionario = {'estado_no_iniciada': ruta['estado_no_iniciada'], 'prioridad': 2}
                    ruta['estado'] = diccionario
                ruta.pop('estado_finalizado')
                ruta.pop('estado_en_curso')
                ruta.pop('estado_no_iniciada')
                ruta['fecha_creacion'] = str(ruta['fecha_creacion'])
                ruta['ultimo_cambio'] = str(ruta['ultimo_cambio'])
                ruta['fecha_inicio'] = str(ruta['fecha_inicio'])
                ruta['fecha_fin'] = str(ruta['fecha_fin'])
                ruta['requisitos'] = DetalleRequisito.get_requisito_x_ruta(ruta['id'])
                ruta['colaboraciones'] = DetalleColaboracion.get_colaboracion_x_ruta(ruta['id'])
                ruta['tipoRuta'] = DetalleEtiquetaRuta.get_tiporuta_x_ruta(ruta['id'])
                ruta['fotos'] = DetalleArchivoRuta.get_archivo_x_ruta(ruta['id'])
                ruta['participantes'] = InscripcionRuta.get_participantes(ruta['id'])
                for participante in ruta['participantes']:
                    detalles = DetalleColaboracionInscripcion.objects.filter(user_id=participante['id'], ruta_id=ruta['id'])
                    colaboraciones_user = []
                    for detalle in detalles:
                        colaboracion = get_or_none(Colaboracion, id=detalle.colaboracion_id)
                        colaboraciones_user.append(colaboracion.nombre)
                    participante['colaboraciones'] = colaboraciones_user
                ubicacion = get_or_none(Ubicacion, id=ruta['ubicacion_id'])
                coordenada_x = get_or_none(Coordenada, id=ubicacion.coordenada_x_id)
                coordenada_y = get_or_none(Coordenada, id=ubicacion.coordenada_y_id)
                dicc = {
                    "coordinateX": {
                        "latitude": float(coordenada_x.latitud),
                        "longitude": float(coordenada_x.longitud)
                    },
                    "coordinateY": {
                        "latitude": float(coordenada_y.latitud),
                        "longitude": float(coordenada_y.longitud)
                    }
                }
                ruta['ubicacion'] = dicc
                ruta.pop('ubicacion_id')
                if get_or_none(InscripcionRuta, ruta_id=ruta['id'], user=token.user) is not None:
                    ruta['inscrito'] = True
                else:
                    ruta['inscrito'] = False

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_rutas', methods=['get'])
    def get_rutas(self, request):
        try:
            data = []
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                data = Ruta.get_rutas(admin=0)
            else:
                data = Ruta.get_rutas(admin=1)

            for ruta in data:
                if ruta['cancelada'] == 1:
                    diccionario = {'estado_cancelado': 1, 'prioridad': 4}
                    ruta['estado'] = diccionario
                elif ruta['finalizado'] == True:
                    diccionario = {'estado_finalizado': ruta['estado_finalizado'], 'prioridad': 5}
                    ruta['estado'] = diccionario
                elif ruta['estado_en_curso'] == True:
                    diccionario = {'estado_en_curso': ruta['estado_en_curso'], 'prioridad': 1}
                    ruta['estado'] = diccionario
                elif ruta['estado_finalizado'] == True:
                    diccionario = {'estado_finalizado': ruta['estado_finalizado'], 'prioridad': 5}
                    ruta['estado'] = diccionario
                elif ruta['cupos_disponibles'] is not None:
                    if ruta['cupos_disponibles'] <= 0:
                        diccionario = {'estado_sin_cupos': 1, 'prioridad': 3}
                        ruta['estado'] = diccionario
                    elif ruta['estado_no_iniciada'] == True:
                        diccionario = {'estado_no_iniciada': ruta['estado_no_iniciada'], 'prioridad': 2}
                        ruta['estado'] = diccionario
                elif ruta['estado_no_iniciada'] == True:
                    diccionario = {'estado_no_iniciada': ruta['estado_no_iniciada'], 'prioridad': 2}
                    ruta['estado'] = diccionario
                ruta.pop('estado_finalizado')
                ruta.pop('estado_en_curso')
                ruta.pop('estado_no_iniciada')
                ruta['fecha_creacion'] = str(ruta['fecha_creacion'])
                ruta['ultimo_cambio'] = str(ruta['ultimo_cambio'])
                ruta['fecha_inicio'] = str(ruta['fecha_inicio'])
                ruta['fecha_fin'] = str(ruta['fecha_fin'])
                ruta['requisitos'] = DetalleRequisito.get_requisito_x_ruta(ruta['id'])
                ruta['colaboraciones'] = DetalleColaboracion.get_colaboracion_x_ruta(ruta['id'])
                ruta['tipoRuta'] = DetalleEtiquetaRuta.get_tiporuta_x_ruta(ruta['id'])
                ruta['fotos'] = DetalleArchivoRuta.get_archivo_x_ruta(ruta['id'])
                ruta['participantes'] = InscripcionRuta.get_participantes(ruta['id'])
                for participante in ruta['participantes']:
                    detalles = DetalleColaboracionInscripcion.objects.filter(user_id=participante['id'], ruta_id=ruta['id'])
                    colaboraciones_user = []
                    for detalle in detalles:
                        colaboracion = get_or_none(Colaboracion, id=detalle.colaboracion_id)
                        colaboraciones_user.append(colaboracion.nombre)
                    participante['colaboraciones'] = colaboraciones_user
                ubicacion = get_or_none(Ubicacion, id=ruta['ubicacion_id'])
                coordenada_x = get_or_none(Coordenada, id=ubicacion.coordenada_x_id)
                coordenada_y = get_or_none(Coordenada, id=ubicacion.coordenada_y_id)
                dicc = {
                    "coordinateX": {
                        "latitude": float(coordenada_x.latitud),
                        "longitude": float(coordenada_x.longitud)
                    },
                    "coordinateY": {
                        "latitude": float(coordenada_y.latitud),
                        "longitude": float(coordenada_y.longitud)
                    }
                }
                ruta['ubicacion'] = dicc
                ruta.pop('ubicacion_id')
                if get_or_none(InscripcionRuta,ruta_id=ruta['id'],user=token.user) is not None:
                    ruta['inscrito'] = True
                else:
                    ruta['inscrito'] = False


            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='inscribirse_ruta', methods=['post'])
    def inscribirse_ruta(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            if data.get('token'):
                inscripcion = InscripcionRuta()
                inscripcion.user = token.user
                ruta = Ruta.objects.get(token=data["token"])
                if ruta.cupos_disponibles is not None:
                    if ruta.cupos_disponibles == 0:
                        return jsonx({'status': 'error', 'message': 'No hay cupos disponibles en esta ruta.'})
                    ruta.cupos_disponibles = ruta.cupos_disponibles - 1
                    ruta.save()
                inscripcion_validate = get_or_none(InscripcionRuta,user=token.user, ruta=ruta)
                if inscripcion_validate:
                    return jsonx({'status': 'error', 'message': 'Ya este usuario esta registrado en esa ruta.'})
                inscripcion.ruta = ruta
                inscripcion.save()
                if data.get('colaboraciones'):
                    for colaboracion_token in data['colaboraciones']:
                        colaboracion_save = get_or_none(Colaboracion, token=colaboracion_token)
                        if colaboracion_save is not None:
                            detalle_colaboracion = DetalleColaboracionInscripcion()
                            detalle_colaboracion.colaboracion = colaboracion_save
                            detalle_colaboracion.ruta = ruta
                            detalle_colaboracion.user = token.user
                            detalle_colaboracion.save()
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Inscripción guardada con éxito.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='cancelar_inscripcion', methods=['post'])
    def cancelar_inscripcion(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            ruta = Ruta.objects.get(token=data["token"])
            inscripcion = get_or_none(InscripcionRuta, user=token.user, ruta=ruta)
            if inscripcion:
                inscripcion.delete()
                detalles = DetalleColaboracionInscripcion.objects.filter(user=token.user, ruta=ruta)
                for detalle in detalles:
                    detalle.delete()
            else:
                return jsonx({'status': 'success', 'message': 'No esta registrado, no se puede eliminar.'})
            if ruta.cupos_disponibles is not None:
                ruta.cupos_disponibles = ruta.cupos_disponibles + 1
                ruta.save()

            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Inscripción eliminada con éxito.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='cancelar_ruta', methods=['post'])
    def cancelar_ruta(self, request):
        try:
            data = request.data
            from rest_framework.authtoken.models import Token
            ruta = Ruta.objects.get(token=data["token"])
            ruta.cancelada = True
            ruta.motivo_cancelacion = data['motivo_cancelacion']
            ruta.save()
            return jsonx({'status': 'success', 'message': 'Se canceló con éxito la ruta.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='aprobar_ruta', methods=['post'])
    def aprobar_ruta(self, request):
        try:
            data = request.data
            from rest_framework.authtoken.models import Token
            ruta = Ruta.objects.get(token=data["token_ruta"])
            ruta.aprobado = True
            ruta.save()
            return jsonx({'status': 'success', 'message': 'Se aprobó con éxito la ruta.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='filtro_inscrito', methods=['get'])
    def filtro_inscrito(self, request):
        try:
            data = []
            data2 = []
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                data = Ruta.get_rutas(admin=0)
            else:
                data = Ruta.get_rutas(admin=1)

            for ruta in data:
                if ruta['estado_finalizado'] == True:
                    diccionario = {'estado_finalizado': ruta['estado_finalizado']}
                    ruta['estado'] = diccionario
                if ruta['estado_en_curso'] == True:
                    diccionario = {'estado_en_curso': ruta['estado_en_curso']}
                    ruta['estado'] = diccionario
                if ruta['estado_no_iniciada'] == True:
                    diccionario = {'estado_no_iniciada': ruta['estado_no_iniciada']}
                    ruta['estado'] = diccionario
                ruta.pop('estado_finalizado')
                ruta.pop('estado_en_curso')
                ruta.pop('estado_no_iniciada')
                ruta['fecha_creacion'] = str(ruta['fecha_creacion'])
                ruta['ultimo_cambio'] = str(ruta['ultimo_cambio'])
                ruta['fecha_inicio'] = str(ruta['fecha_inicio'])
                ruta['fecha_fin'] = str(ruta['fecha_fin'])
                ruta['requisitos'] = DetalleRequisito.get_requisito_x_ruta(ruta['id'])
                ruta['colaboraciones'] = DetalleColaboracion.get_colaboracion_x_ruta(ruta['id'])
                ruta['tipoRuta'] = DetalleEtiquetaRuta.get_tiporuta_x_ruta(ruta['id'])
                ruta['fotos'] = DetalleArchivoRuta.get_archivo_x_ruta(ruta['id'])
                ruta['participantes'] = InscripcionRuta.get_participantes(ruta['id'])
                if get_or_none(InscripcionRuta, ruta_id=ruta['id'], user=token.user) is not None:
                    ruta['inscrito'] = True
                    data2.append(ruta)
                else:
                    ruta['inscrito'] = False

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data2})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='filtro_cancelada', methods=['get'])
    def filtro_cancelada(self, request):
        try:
            data = []
            data2 = []
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                data = Ruta.get_rutas(admin=0)
            else:
                data = Ruta.get_rutas(admin=1)

            for ruta in data:
                if ruta['estado_finalizado'] == True:
                    diccionario = {'estado_finalizado': ruta['estado_finalizado']}
                    ruta['estado'] = diccionario
                if ruta['estado_en_curso'] == True:
                    diccionario = {'estado_en_curso': ruta['estado_en_curso']}
                    ruta['estado'] = diccionario
                if ruta['estado_no_iniciada'] == True:
                    diccionario = {'estado_no_iniciada': ruta['estado_no_iniciada']}
                    ruta['estado'] = diccionario
                ruta.pop('estado_finalizado')
                ruta.pop('estado_en_curso')
                ruta.pop('estado_no_iniciada')
                ruta['fecha_creacion'] = str(ruta['fecha_creacion'])
                ruta['ultimo_cambio'] = str(ruta['ultimo_cambio'])
                ruta['fecha_inicio'] = str(ruta['fecha_inicio'])
                ruta['fecha_fin'] = str(ruta['fecha_fin'])
                ruta['requisitos'] = DetalleRequisito.get_requisito_x_ruta(ruta['id'])
                ruta['colaboraciones'] = DetalleColaboracion.get_colaboracion_x_ruta(ruta['id'])
                ruta['tipoRuta'] = DetalleEtiquetaRuta.get_tiporuta_x_ruta(ruta['id'])
                ruta['fotos'] = DetalleArchivoRuta.get_archivo_x_ruta(ruta['id'])
                ruta['participantes'] = InscripcionRuta.get_participantes(ruta['id'])
                if get_or_none(InscripcionRuta, ruta_id=ruta['id'], user=token.user) is not None:
                    ruta['inscrito'] = True
                else:
                    ruta['inscrito'] = False
                if ruta['cancelada'] == True:
                    data2.append(ruta)

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data2})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='filtro_estado', methods=['post'])
    def filtro_estado(self, request):
        try:
            data = []
            data2 = []
            data_request = request.data
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                data = Ruta.get_rutas(admin=0)
            else:
                data = Ruta.get_rutas(admin=1)

            for ruta in data:
                ruta['fecha_creacion'] = str(ruta['fecha_creacion'])
                ruta['ultimo_cambio'] = str(ruta['ultimo_cambio'])
                ruta['fecha_inicio'] = str(ruta['fecha_inicio'])
                ruta['fecha_fin'] = str(ruta['fecha_fin'])
                ruta['requisitos'] = DetalleRequisito.get_requisito_x_ruta(ruta['id'])
                ruta['colaboraciones'] = DetalleColaboracion.get_colaboracion_x_ruta(ruta['id'])
                ruta['tipoRuta'] = DetalleEtiquetaRuta.get_tiporuta_x_ruta(ruta['id'])
                ruta['fotos'] = DetalleArchivoRuta.get_archivo_x_ruta(ruta['id'])
                ruta['participantes'] = InscripcionRuta.get_participantes(ruta['id'])
                if get_or_none(InscripcionRuta, ruta_id=ruta['id'], user=token.user) is not None:
                    ruta['inscrito'] = True
                else:
                    ruta['inscrito'] = False

                if ruta['estado_finalizado'] == True:
                    diccionario = {'estado_finalizado': ruta['estado_finalizado']}
                    ruta['estado'] = diccionario
                    if data_request['estado'] == 'finalizado':
                        data2.append(ruta)

                if ruta['estado_en_curso'] == True:
                    diccionario = {'estado_en_curso': ruta['estado_en_curso']}
                    ruta['estado'] = diccionario
                    if data_request['estado'] == 'en_curso':
                        data2.append(ruta)

                if ruta['estado_no_iniciada'] == True:
                    diccionario = {'estado_no_iniciada': ruta['estado_no_iniciada']}
                    ruta['estado'] = diccionario
                    if data_request['estado'] == 'pendiente':
                        data2.append(ruta)

                ruta.pop('estado_finalizado')
                ruta.pop('estado_en_curso')
                ruta.pop('estado_no_iniciada')

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data2})
        except ApplicationError as msg:
            print(msg)
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            print(e)
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='eliminar_ruta', methods=['post'])
    def eliminar_ruta(self, request):
        try:
            data = request.data
            from rest_framework.authtoken.models import Token
            ruta = Ruta.objects.get(token=data["token_ruta"])

            detalles_requisitos = DetalleRequisito.objects.filter(ruta=ruta)
            for detalle_requisito in detalles_requisitos:
                detalle_requisito.delete()

            detalles_colaboracion = DetalleColaboracion.objects.filter(ruta=ruta)
            for detalle_requisito in detalles_colaboracion:
                detalle_requisito.delete()

            detalles_etiquetaruta = DetalleEtiquetaRuta.objects.filter(ruta=ruta)
            for detalle_etiquetaruta in detalles_etiquetaruta:
                detalle_etiquetaruta.delete()

            detalles_archivoruta = DetalleArchivoRuta.objects.filter(ruta=ruta)
            for detalle_archivoruta in detalles_archivoruta:
                detalle_archivoruta.delete()

            detalles_inscripcionruta = InscripcionRuta.objects.filter(ruta=ruta)
            for detalle_inscripcionruta in detalles_inscripcionruta:
                detalle_inscripcionruta.delete()

            #FALTA ELIMINAR COORDINADA Y EL RASTREO DE RUTA, EL ARCHIVO IGUAL

            ruta.delete()
            return jsonx({'status': 'success', 'message': 'Se ha eliminado con éxito la ruta.'})

        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='editar_ruta', methods=['post'])
    def editar_ruta(self, request):
        transaction.set_autocommit(False)
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                return jsonx({'status': 'error', 'message': 'Solo pueden editar rutas los administradores.'})

            data = request.data
            ruta = Ruta.objects.get(token=data["token_ruta"])

            detalles_requisitos = DetalleRequisito.objects.filter(ruta=ruta)
            for detalle_requisito in detalles_requisitos:
                detalle_requisito.delete()

            detalles_colaboracion = DetalleColaboracion.objects.filter(ruta=ruta)
            for detalle_requisito in detalles_colaboracion:
                detalle_requisito.delete()

            detalles_etiquetaruta = DetalleEtiquetaRuta.objects.filter(ruta=ruta)
            for detalle_etiquetaruta in detalles_etiquetaruta:
                detalle_etiquetaruta.delete()

            detalles_archivoruta = DetalleArchivoRuta.objects.filter(ruta=ruta)
            for detalle_archivoruta in detalles_archivoruta:
                detalle_archivoruta.delete()

            #Eliminar ubicacion

            ruta.nombre = data['nombre']
            ruta.descripcion = data['descripcion']
            ruta.estado = 'Disponible'
            if data.get('cupos_disponibles'):
                ruta.cupos_disponibles = data['cupos_disponibles']
            ruta.lugar = data['lugar']
            ruta.fecha_inicio = data['fecha_inicio']
            ruta.fecha_fin = data['fecha_fin']
            ruta.user = token.user
            coordenadax = Coordenada.objects.create(latitud=data['ubicacion']['coordinateX']['latitude'],
                                                    longitud=data['ubicacion']['coordinateX']['longitude'])
            coordenaday = Coordenada.objects.create(latitud=data['ubicacion']['coordinateY']['latitude'],
                                                    longitud=data['ubicacion']['coordinateY']['longitude'])
            ubicacion = Ubicacion.objects.create(coordenada_x=coordenadax, coordenada_y=coordenaday)
            ruta.ubicacion = ubicacion
            ruta.save()

            if data.get('requisitos'):
                for requisito_token in data['requisitos']:
                    requisito_save = get_or_none(Requisito, token=requisito_token)
                    if requisito_save is not None:
                        detalle_requisito = DetalleRequisito()
                        detalle_requisito.requisito = requisito_save
                        detalle_requisito.ruta = ruta
                        detalle_requisito.save()

            if data.get('colaboraciones'):
                for colaboracion_token in data['colaboraciones']:
                    colaboracion_save = get_or_none(Colaboracion, token=colaboracion_token)
                    if colaboracion_save is not None:
                        detalle_colaboracion = DetalleColaboracion()
                        detalle_colaboracion.colaboracion = colaboracion_save
                        detalle_colaboracion.ruta = ruta
                        detalle_colaboracion.save()

            if data.get('tipoRuta'):
                for token_tipo_ruta in data['tipoRuta']:
                    etiqueta_ruta = get_or_none(EtiquetaRuta, token=token_tipo_ruta)
                    if etiqueta_ruta is not None:
                        detalle_etiqueta_ruta = DetalleEtiquetaRuta()
                        detalle_etiqueta_ruta.ruta = ruta
                        detalle_etiqueta_ruta.etiqueta = etiqueta_ruta
                        detalle_etiqueta_ruta.save()

            if data.get('fotos'):
                for elemento in data['fotos']:
                    archivo = Archivo()
                    archivo.link = elemento['link']
                    archivo.tipo = 'imagen'
                    archivo.path = elemento['path']
                    archivo.save()
                    detalle_archivo_ruta = DetalleArchivoRuta()
                    detalle_archivo_ruta.archivo = archivo
                    detalle_archivo_ruta.ruta = ruta
                    detalle_archivo_ruta.save()

            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Ruta editada con éxito.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='finalizar_ruta', methods=['post'])
    def finalizar_ruta(self, request):
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                return jsonx({'status': 'error', 'message': 'Solo pueden finalizar las rutas los administradores.'})
            data = request.data
            ruta = Ruta.objects.get(token=data["token_ruta"])
            ruta.finalizado = True
            ruta.save()
            return jsonx({'status': 'success', 'message': 'Ruta finalizada con éxito.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='safe_in_home', methods=['post'])
    def safe_in_home(self, request):
        transaction.set_autocommit(False)
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            data = request.data
            ruta = Ruta.objects.get(token=data["token_ruta"])
            safe = data["safe"]
            inscripcion_ruta = get_or_none(InscripcionRuta, ruta=ruta, user=token.user)
            if inscripcion_ruta is None:
                return jsonx({'status': 'success', 'message': 'No esta registrado este participante en esta ruta.'})
            inscripcion_ruta.safe = safe
            inscripcion_ruta.save()
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Seguro en casa.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_not_response', methods=['get'])
    def get_not_response(self, request):
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            data = InscripcionRuta.get_not_response(token.user.id)

            return jsonx({'status': 'success', 'message': 'Listado de inscripciones devuelto con exito.', 'data':data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})