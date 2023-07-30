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
                    token_usuario.append(user_data['token_notificacion'])
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
                            token_usuario.append(usuarioDetalle.token_notificacion)
                            participacionAlerta, created = ParticipacionAlerta.objects.get_or_create(user=usuario, alerta=alerta, isAsistencia=0)
                            if created:
                                participacionAlerta.save()
                        
                    elif tipoUsuario == "Miembros":
                        usuarios_miembros = [user_data for user_data in usuarios if user_data['tipo'] == "Miembro"]
                        for user_data in usuarios_miembros:
                            usuario = User.objects.get(id=user_data['usuario_id'])
                            usuarioDetalle=get_or_none(DetalleUsuario, usuario_id=usuario.id)
                            token_usuario.append(usuarioDetalle.token_notificacion)
                            participacionAlerta, created = ParticipacionAlerta.objects.get_or_create(user=usuario, alerta=alerta, isAsistencia=0)
                            if created:
                                participacionAlerta.save()
            
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Alerta creada con éxito.', 'data':token_usuario})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    
    @action(detail=False, url_path='get_alertas_enviadas', methods=['get'])
    def get_alertas_enviadas(self, request):
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            data= Alerta.get_alertas_de_usuario(token.user_id)
            for alerta in data:
                alerta['fecha_creacion'] = alerta['fecha_creacion']- timedelta(hours=5)
                alerta['fecha_creacion'] = alerta['fecha_creacion'].isoformat()

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_alertas_recibidas', methods=['get'])
    def get_alertas_recibidas(self, request):
        try:
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            data= Alerta.get_alertas_recibidas(token.user_id)
            for alerta in data:
                alerta['fecha_creacion'] = alerta['fecha_creacion']- timedelta(hours=5)
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
                alerta['fecha_creacion'] = alerta['fecha_creacion']- timedelta(hours=5)
                alerta['fecha_creacion'] = alerta['fecha_creacion'].isoformat()
                alerta['fecha_fin'] = str(alerta['fecha_fin'])
                alerta['tipo'] = alerta['nombre']
                alerta['multimedia'] = ArchivoAlerta.get_archivo_x_alerta(alerta['id'])
                alerta['comentarios'] = ComentarioAlerta.get_comentario_x_alerta(alerta['id'])
                for comentario in alerta['comentarios']:
                    comentario['fecha_creacion'] = comentario['fecha_creacion']- timedelta(hours=5)
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

    

    # @action(detail=False, url_path='new_etiqueta', methods=['post'])
    # def new_etiqueta(self, request):
    #     try:
    #         data = request.data
    #         etiqueta= EtiquetaAlerta()
    #         etiqueta.nombre=data['nombre']
    #         etiqueta.value=data['value']
    #         etiqueta.save()
    #         return jsonx({'status': 'success', 'message': 'Etiqueta creada.'})
    #     except ApplicationError as msg:
    #         return jsonx({'status': 'error', 'message': str(msg)})
    #     except Exception as e:
    #         return jsonx({'status': 'error', 'message': str(e)})