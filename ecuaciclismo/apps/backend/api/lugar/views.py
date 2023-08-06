from django.db import transaction
from django.forms import ValidationError
from rest_framework import viewsets
from datetime import datetime
from datetime import timedelta
from ecuaciclismo.apps.backend.api.alerta.AlertaSerializer import AlertaSerializer
from ecuaciclismo.apps.backend.api.lugar.LugarSerializer import LugarSerializer
from ecuaciclismo.apps.backend.lugar.models import Ciclovia, Local, Lugar, Parqueadero, Servicio
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

class LugarViewSet(viewsets.ModelViewSet):
    serializer_class= LugarSerializer
    queryset = Lugar.objects.all()
    
    def get_queryset(self):
        queryset = self.queryset
        return queryset
    
    @action(detail=False, url_path ='new_lugar', methods=['post'])
    def new_lugar(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            tipo_lugar= data['tipo_lugar']
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])

            if tipo_lugar not in ['parqueadero','ciclovia','local']:
                raise ApplicationError('Tipo de lugar no valido')
            
            if tipo_lugar== 'local':
                lugar = Local()
                if data['isVerificado']==1:
                    lugar.user=token.user
                    
                    lugar.servicio=get_or_none(Servicio, nombre=data['servicio'])
                    lugar.celular=data['celular']
                    lugar.hora_fin=datetime.strptime(data['hora_fin'], '%H:%M:%S').time()   
                    lugar.hora_inicio=datetime.strptime(data['hora_inicio'], '%H:%M:%S').time()
                    lugar.isBeneficios = data['isBeneficios']
                    lugar.isVerificado = data['isVerificado']

            
            elif tipo_lugar == 'parqueadero':
                lugar = Parqueadero()
                lugar.capacidad = data['capacidad']
                lugar.tarifa = data['tarifa']
            else:
                lugar = Ciclovia()
                lugar.longitud = data['longitud']

            lugar.nombre = data['nombre']
            lugar.descripcion = data['descripcion']
            lugar.direccion = data['direccion']
            lugar.imagen = data['imagen']
            
            coordenadax = Coordenada.objects.create(latitud=data['ubicacion']['coordinateX']['latitude'],longitud=data['ubicacion']['coordinateX']['longitude'])
            coordenaday = Coordenada.objects.create(latitud=data['ubicacion']['coordinateY']['latitude'],longitud=data['ubicacion']['coordinateY']['longitude'])
            ubicacion = Ubicacion.objects.create(coordenada_x=coordenadax, coordenada_y=coordenaday)
            lugar.ubicacion = ubicacion
            # Verificar si los datos del lugar son válidos
            lugar.save()

            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Lugar creado con éxito.'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})
    @action(detail=False, url_path ='get_lugares', methods=['get'])
    def get_lugares(self, request):
        try:
            lugares = Lugar.get_lugares(1)
            for lugar in lugares:
                ubicacion = get_or_none(Ubicacion, id=lugar['ubicacion'])
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
                lugar['ubicacion'] = dicc

            return jsonx({'status': 'success', 'lugares': lugares})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
        
    @action(detail=False, url_path ='get_lugar', methods=['post'])
    def get_lugar(self, request):
        try:
            dato= request.data
            lugar=get_or_none(Lugar, token=dato['token_lugar'])
            dataLugar = Lugar.getLugarById(lugar.id)
            
            print(dataLugar)
            ubicacion = get_or_none(Ubicacion, id=dataLugar['ubicacion'])
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
            dataLugar['ubicacion'] = dicc
            if dataLugar['tipo'] == 'local':
                local=Local.getLocalById(lugar.id)
                print(local)
                if local['local_seguro']==1:
                    dataLugar['servicio']=get_or_none(Servicio, id=local['servicio']).nombre
                    dataLugar['celular']=local['celular']
                    dataLugar['hora_inicio']=local['hora_inicio'].strftime('%H:%M:%S')
                    dataLugar['hora_fin']=local['hora_fin'].strftime('%H:%M:%S')
                    dataLugar['hora_inicio']=str(dataLugar['hora_inicio'])
                    dataLugar['hora_fin']=str(dataLugar['hora_fin'])
                    dataLugar['isBeneficios']=local['isBeneficios']
                    dataLugar['local_seguro']=local['local_seguro']
                    dataLugar['nombre_propietario']=local['nombre_propietario']
                    dataLugar['apellido_propietario']=local['apellido_propietario']
            elif dataLugar['tipo'] == 'parqueadero':
                parqueadero=Parqueadero.getParqueaderoById(lugar.id)
                dataLugar['capacidad']=parqueadero['capacidad']
                dataLugar['tarifa']=parqueadero['tarifa']
            elif dataLugar['tipo'] == 'ciclovia':
                ciclovia=Ciclovia.getCicloviaById(lugar.id)
                dataLugar['longitud']=ciclovia['longitud']
            return jsonx({'status': 'success', 'lugar': dataLugar})
        
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
    @action(detail=False, url_path ='new_servicio', methods=['post'])
    def new_servicio(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            servicio = Servicio()
            servicio.nombre = data['nombre']
            servicio.valor = data['valor']
            servicio.save()
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Servicio creado con éxito.'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})


