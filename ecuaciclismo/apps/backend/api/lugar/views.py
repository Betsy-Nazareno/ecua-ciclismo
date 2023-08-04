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


