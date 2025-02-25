from django.db import transaction
from rest_framework import viewsets
from datetime import datetime
from datetime import timedelta
from ecuaciclismo.apps.backend.api.alerta.AlertaSerializer import AlertaSerializer
from ecuaciclismo.apps.backend.ruta.models import Ruta, Coordenada, Ubicacion, DetalleRequisito, \
    Colaboracion,Archivo
from ecuaciclismo.apps.backend.alerta.models import Alerta, ComentarioAlerta, DetalleColaboracion,EtiquetaAlerta, ArchivoAlerta, ParticipacionAlerta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from ecuaciclismo.apps.backend.usuario.models import ContactoSeguro, GrupoContactoSeguro, DetalleUsuario
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none
from rest_framework.authtoken.models import Token
from ecuaciclismo.helpers.jsonx import jsonx
from django.utils import timezone

class AlertaViewSet(viewsets.ModelViewSet):

    serializer_class = AlertaSerializer
    queryset = Alerta.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset
    
    @action(detail=False, url_path='new_alerta', methods=['post'])
    def new_alerta(self, request):
        transaction.set_autocommit(False)
        token_usuario=[]
        token_usuarios_negocio = []
        
        try:
            data = request.data
            alerta = Alerta()
            alerta.estado = 'En curso'
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            alerta.user =token.user
    
            alerta.etiqueta=get_or_none(EtiquetaAlerta, nombre=data['etiqueta'])
            if not data.get('descripcion'):
                alerta.descripcion=(get_or_none(EtiquetaAlerta, nombre=data['etiqueta']).value)
            else:
                alerta.descripcion = data['descripcion']
            coordenadax = Coordenada.objects.create(latitud=data['ubicacion']['coordinateX']['latitude'],longitud=data['ubicacion']['coordinateX']['longitude'])
            coordenaday = Coordenada.objects.create(latitud=data['ubicacion']['coordinateY']['latitude'],longitud=data['ubicacion']['coordinateY']['longitude'])
            ubicacion = Ubicacion.objects.create(coordenada_x=coordenadax, coordenada_y=coordenaday)
            alerta.ubicacion = ubicacion
            alerta.save()

            if data.get('colaboraciones'):
                for colaboracion_token in data['colaboraciones']:
                    colaboracion_save = get_or_none(Colaboracion, token=colaboracion_token)
                    if colaboracion_save is not None:
                        detalle_colaboracion = DetalleColaboracion()
                        detalle_colaboracion.colaboracion = colaboracion_save
                        detalle_colaboracion.alerta = alerta
                        detalle_colaboracion.save()


            if data.get('multimedia'):
                for elemento in data['multimedia']:
                    archivo = Archivo()
                    archivo.link = elemento['link']
                    archivo.tipo = elemento['tipo']
                    archivo.path = elemento['path']
                    archivo.save()
                    archivo_alerta = ArchivoAlerta()
                    archivo_alerta.archivo = archivo
                    archivo_alerta.alerta = alerta
                    archivo_alerta.save()


            if data['visibilidad']:
                usuarios=DetalleUsuario.get_all_users()
                locales=[user_data for user_data in usuarios if user_data['isPropietary'] == 1]
                for user_data in locales:
                    usuarioDetalle = get_or_none(DetalleUsuario, usuario_id=user_data['usuario_id'])
                    if usuarioDetalle.silenciar_notificaciones == 0:
                        token_usuarios_negocio.append(usuarioDetalle.token_notificacion)
                    usuario = User.objects.get(id=user_data['usuario_id'])
                    participacionAlerta, created = ParticipacionAlerta.objects.get_or_create(user=usuario, alerta=alerta, isAsistencia=0)
                    if created:
                        participacionAlerta.save()

                for tipoUsuario in data['visibilidad']:
                    if tipoUsuario=="Contactos seguros":
                        
                        contactos=GrupoContactoSeguro.get_contactos_seguros_usuario(alerta.user_id)
                        for contacto in contactos:
                            cs=get_or_none(ContactoSeguro, token=contacto['token'])
                            if cs.isUser==1:
                                usuario=User.objects.get(id=cs.user_id)
                                usuarioDetalle=get_or_none(DetalleUsuario, usuario_id=usuario.id)
                                if usuarioDetalle.silenciar_notificaciones == 0 and not usuarioDetalle.isPropietary:
                                    token_usuario.append(usuarioDetalle.token_notificacion)
                                participacionAlerta=ParticipacionAlerta()
                                participacionAlerta, created = ParticipacionAlerta.objects.get_or_create(user=usuario, alerta=alerta, isAsistencia = 0)
                                if created:
                                    participacionAlerta.save()

                    elif tipoUsuario=="Verificados":
                        usuarios_verificados = [user_data for user_data in usuarios if user_data['tipo'] == "Verificado"]
                        for user_data in usuarios_verificados:
                            usuario = User.objects.get(id=user_data['usuario_id'])
                            usuarioDetalle=get_or_none(DetalleUsuario, usuario_id=usuario.id)
                            
                            if usuarioDetalle.silenciar_notificaciones == 0 and not usuarioDetalle.isPropietary:
                                token_usuario.append(usuarioDetalle.token_notificacion)
                            participacionAlerta, created = ParticipacionAlerta.objects.get_or_create(user=usuario, alerta=alerta, isAsistencia=0)
                            if created:
                                participacionAlerta.save()
                        
                    elif tipoUsuario == "Miembros":
                        usuarios_miembros = [user_data for user_data in usuarios if user_data['tipo'] == "Miembro"]
                        for user_data in usuarios_miembros:
                            usuario = User.objects.get(id=user_data['usuario_id'])
                            usuarioDetalle=get_or_none(DetalleUsuario, usuario_id=usuario.id)
                            if usuarioDetalle.silenciar_notificaciones == 0 and not usuarioDetalle.isPropietary:
                                token_usuario.append(usuarioDetalle.token_notificacion)
                            participacionAlerta, created = ParticipacionAlerta.objects.get_or_create(user=usuario, alerta=alerta, isAsistencia=0)
                            if created:
                                participacionAlerta.save()
            
            transaction.commit()
            
            token_usuario = [ token for token in token_usuario if token is not None ]
            token_usuarios_negocio = [ token for token in token_usuarios_negocio if token is not None ]
            return jsonx({'status': 'success', 'message': 'Alerta creada con éxito.', 'data':token_usuario, 'token_usuarios_negocio':token_usuarios_negocio})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})
    @action(detail=False, url_path='confirmar_asistencia', methods=['post'])
    def confirmar_asistencia(self, request):
        try:
            data = request.data
            alerta = Alerta.objects.get(token=data['token_alerta'])
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            participacionAlerta = ParticipacionAlerta.objects.get(user=token.user, alerta=alerta)
            participacionAlerta.isAsistencia = 1
            participacionAlerta.save()
            return jsonx({'status': 'success', 'message': 'Se confirmo la asistencia a la alerta.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='update_alerta', methods=['post'])
    def update_alerta(self, request):
        try:
            data = request.data
            alerta = Alerta.objects.get(token=data['token_alerta'])
            Alerta.update_estado(alerta.id, data['estado'], data['motivo_cancelacion'])
            return jsonx({'status': 'success', 'message': 'Alerta actualizada con éxito.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_alertas_enviadas', methods=['get'])
    def get_alertas_enviadas(self, request):
        try:
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            data= Alerta.get_alertas_de_usuario(token.user_id)
            for alerta in data:
                alerta['fecha_creacion'] = alerta['fecha_creacion']+ timedelta(hours=5)
                alerta['fecha_creacion'] = alerta['fecha_creacion'].isoformat()

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_alertas_recibidas', methods=['get'])
    def get_alertas_recibidas(self, request):
        try:
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            data= Alerta.get_alertas_recibidas(token.user_id)
            for alerta in data:
                alerta['fecha_creacion'] = alerta['fecha_creacion']+ timedelta(hours=5)
                alerta['fecha_creacion'] = alerta['fecha_creacion'].isoformat()

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})


    @action(detail=False, url_path='get_alerta', methods=['post'])
    def get_alerta(self, request):
        try:
            dato = request.data
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            id_user = token.user.id
            dataAlerta = Alerta.get_alerta(dato['token_alerta'])
            for alerta in dataAlerta:
                alerta['fecha_creacion'] = alerta['fecha_creacion']+ timedelta(hours=5)
                alerta['fecha_creacion'] = alerta['fecha_creacion'].isoformat()
                alerta['fecha_fin'] = str(alerta['fecha_fin'])
                alerta['tipo'] = alerta['nombre']
                alerta['multimedia'] = ArchivoAlerta.get_archivo_x_alerta(alerta['id'])
                alerta['comentarios'] = ComentarioAlerta.get_comentario_x_alerta(alerta['id'])
                for comentario in alerta['comentarios']:
                    comentario['fecha_creacion'] = comentario['fecha_creacion']+ timedelta(hours=5)
                    comentario['fecha_creacion'] = comentario['fecha_creacion'].isoformat()
                alerta['participantes']= ParticipacionAlerta.get_asistentes(alerta['id'])
                alerta['colaboraciones'] = DetalleColaboracion.get_colaboracion_x_alerta(alerta['id'])
                
                ubicacion = get_or_none(Ubicacion, id=alerta['ubicacion_id'])
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
                alerta['ubicacion'] = dicc
                alerta.pop('ubicacion_id')
                alerta.pop('nombre')
                alerta.pop('etiqueta_id')
            return jsonx({'status': 'success', 'message': 'Información obtenida', 'alerta': alerta})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
    @action(detail=False, url_path='new_comentario_alerta', methods=['post'])
    def new_comentario_alerta(self, request):
        try:
            data = request.data

            if data['token_alerta'] is not None and data['token_alerta'] != '':
                alerta = Alerta.objects.get(token=data['token_alerta'])
                token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
                comentario = ComentarioAlerta()
                comentario.alerta = alerta
                comentario.user = token.user
                comentario.comentario = data['comentario']
                comentario.save()

                return jsonx({'status': 'success', 'message': 'Se añadio un comentario a la alerta.'})
            else:
                return jsonx({'status': 'success', 'message': 'El campo token es nulo o vacío.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    

    @action(detail=False, url_path='new_etiqueta', methods=['post'])
    def new_etiqueta(self, request):
        try:
            data = request.data
            etiqueta= EtiquetaAlerta()
            etiqueta.nombre=data['nombre']
            etiqueta.value=data['value']
            etiqueta.save()
            return jsonx({'status': 'success', 'message': 'Etiqueta creada.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
        
    @action(detail=False, url_path='get_ultima_alerta', methods=['get'])
    def get_ultima_alerta(self, request):
        try:
            ultima_alerta = Alerta.objects.latest('fecha_creacion')
            if ultima_alerta.estado != 'En curso':
                return jsonx({'status': 'error', 'message': 'ÚLtima alerta cancelada o atendida.'})

            data = {
                "id": ultima_alerta.id,
                "descripcion": ultima_alerta.descripcion,
                "estado": ultima_alerta.estado,
                "fecha_creacion": ultima_alerta.fecha_creacion.isoformat(),  
                "user": ultima_alerta.user.username if ultima_alerta.user else None,    
                "ubicacion": {
                    "coordenada_x": {
                        "latitude": ultima_alerta.ubicacion.coordenada_x.latitud,
                        "longitude": ultima_alerta.ubicacion.coordenada_x.longitud,
                    },
                    "coordenada_y": {
                        "latitude": ultima_alerta.ubicacion.coordenada_y.latitud,
                        "longitude": ultima_alerta.ubicacion.coordenada_y.longitud,
                    },
                } if ultima_alerta.ubicacion else None,
            }

            return jsonx({'status': 'success', 'message': 'Última alerta en curso obtenida.', 'data': data})

        except Alerta.DoesNotExist:
            return jsonx({'status': 'error', 'message': 'No se encontraron alertas.'})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
