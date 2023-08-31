from django.db import transaction
from django.forms import ValidationError
from datetime import datetime
from ecuaciclismo.apps.backend.api.solicitud.SolicitudSerializer import SolicitudSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from ecuaciclismo.apps.backend.lugar.models import Lugar
from ecuaciclismo.apps.backend.ruta.models import Coordenada, Ubicacion
from ecuaciclismo.apps.backend.solicitud.models import Solicitud, SolicitudLugar, SolicitudVerificado
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none
from rest_framework.authtoken.models import Token
from ecuaciclismo.helpers.jsonx import jsonx

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class= SolicitudSerializer
    queryset = Solicitud.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset
    @action(detail=False, url_path='new_solicitud', methods=['post'])
    def new_solicitud_lugar(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            mensaje = ''
            if data.get('token_lugar') is not None:
                mensaje = 'Solicitud de lugar creado con éxito'
                solicitud = SolicitudLugar()
                lugar=get_or_none(Lugar, token=data['token_lugar'])
                solicitud.lugar = lugar
                if data['path_Pdf']:
                    mensaje = 'Solicitud de registro local creado con éxito'
                    solicitud.path_Pdf=data['path_Pdf']
            else:
                mensaje = 'Solicitud de membresia creado con éxito'
                solicitud = Solicitud()
                solicitud.path_Pdf=data['path_Pdf']
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            solicitud.user = token.user
            solicitud.estado = 'Pendiente'
            solicitud.save()
            transaction.commit()

            return jsonx({'status': 'success', 'message': mensaje})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx(False, str(e))

    @action(detail=False, url_path='new_solicitud_verificado', methods=['post'])
    def new_solicitud_verificado(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            solicitud = SolicitudVerificado()
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            solicitud.user = token.user
            solicitud.descripcion = data['descripcion']
            solicitud.estado = 'Pendiente'
            solicitud.imagen = data['imagen']
            solicitud.save()  # Guardar la instancia primero
        
            # Luego de guardar la instancia, puedes agregar usuarios a la relación many-to-many
            for user in data['users']:
                usuario = User.objects.get(username=user['username'])
                solicitud.usuarios.add(usuario)
        
            transaction.commit()

            return jsonx({'status': 'success', 'message': 'Solicitud de verificación creado con éxito'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})
    @action(detail=False,url_path='get_solicitudes',methods=['get'])
    def get_solicitudes(self,request):
        try:
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            solicitudes= Solicitud.get_all()
            
            for solicitud in solicitudes:
                solicitud['fecha_creacion']=datetime.strftime(solicitud['fecha_creacion'],'%Y-%m-%d %H:%M:%S')
                solicitud['fecha_creacion']=str(solicitud['fecha_creacion'])
                solicitudLugar=get_or_none(SolicitudLugar, id=solicitud['id'])
                if solicitudLugar is not None:
                    solicitud['tipo']="Recomendados"
                    datoLugar=SolicitudLugar.get_by_id(solicitud['id'])
                    solicitud['nombre']=datoLugar[0]['nombre']
                    solicitud['direccion']=datoLugar[0]['direccion']
                    solicitud['descripcion']=datoLugar[0]['descripcion']
                    solicitud['imagen']=datoLugar[0]['imagen']
                    ubicacion = get_or_none(Ubicacion, id=datoLugar[0]['ubicacion_id'])
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
                    solicitud['ubicacion'] = dicc


                    if solicitud.get('path_Pdf') is not None:
                        solicitud['tipo']="Registro Local"
                
                else:
                    solicitud['nombre']="Solicitud Membresia"
                    solicitud['tipo']="Membresia"
                
                solicitudVerificado=get_or_none(SolicitudVerificado, id=solicitud['id'])
                if solicitudVerificado is not None:
                    solicitud['nombre']="Solicitud Verificación"
                    solicitud['tipo']="Verificacion"
                    solicitud['descripcion']=solicitudVerificado.descripcion
                    solicitud['imagen']=solicitudVerificado.imagen
                    solicitud['usuarios']= SolicitudVerificado.get_Usuarios(solicitud['id'])
                    
    
                
            return jsonx({'status': 'success', 'message': 'Solicitudes obtenidas con éxito','solicitudes':solicitudes})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx(False, str(e))
    
    @action(detail=False,url_path='responder_solicitud',methods=['post'])
    def responder_solicitud(self,request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            solicitud = get_or_none(Solicitud, token=data['token_solicitud'])
            solicitud.estado=data['estado']
            solicitud.motivo_rechazo=data['motivo_rechazo']
            print(data['tipo'])
            if(data['tipo']=='Recomendados' or data['tipo']=='Registro Local'):
                solicitudLugar = get_or_none(SolicitudLugar, solicitud_ptr_id=solicitud.id)
                lugar=get_or_none(Lugar, id=solicitudLugar.lugar_id)
                lugar.isActived=True
                lugar.save()
            else:
                detalleUsuario=get_or_none(DetalleUsuario, usuario_id=solicitud.user_id)
                if data['tipo']=='Membresia':
                    detalleUsuario.tipo='Miembro'
                #Aqui va la parte para aprobar la solicitud de verificacion
                detalleUsuario.save()

            solicitud.save()
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Solicitud respondida con éxito'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx(False, str(e))

                