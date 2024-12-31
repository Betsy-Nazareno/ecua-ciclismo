from django.db import transaction
from django.forms import ValidationError
from rest_framework import viewsets
from datetime import datetime
from ecuaciclismo.apps.backend.api.lugar.LugarSerializer import LugarSerializer
from ecuaciclismo.apps.backend.lugar.models import Ciclovia, Local, Lugar, Parqueadero, Servicio, Reseña
from ecuaciclismo.apps.backend.ruta.models import  Coordenada, Ubicacion
from rest_framework import viewsets
from rest_framework.decorators import action
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
                lugar.servicio=get_or_none(Servicio, nombre=data['servicio'])
                if data['isVerificado']==1:
                    lugar.user=token.user
                    lugar.isParqueadero=data['parqueadero']
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
            return jsonx({'status': 'success', 'message': 'Lugar creado con éxito','token_lugar': lugar.token})
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
            puntuacion=Reseña.getPuntuacionesByIdLugar(lugar.id)
            dataLugar['promedio_seguridad']=puntuacion['promedio_seguridad']
            dataLugar['promedio_limpieza']=puntuacion['promedio_limpieza']
            dataLugar['promedio_atencion']=puntuacion['promedio_atencion']
            if dataLugar['tipo'] == 'local':
                lugarLocal=get_or_none(Local, lugar_ptr_id=lugar.id)
                dataLugar['servicio']=lugarLocal.servicio.nombre
                if lugarLocal.isVerificado==1:
                    local=Local.getLocalById(lugar.id)
                    dataLugar['celular']=local['celular']
                    dataLugar['hora_inicio']=local['hora_inicio'].strftime('%H:%M:%S')
                    dataLugar['hora_fin']=local['hora_fin'].strftime('%H:%M:%S')
                    dataLugar['hora_inicio']=str(dataLugar['hora_inicio'])
                    dataLugar['hora_fin']=str(dataLugar['hora_fin'])
                    dataLugar['isBeneficios']=local['isBeneficios']
                    dataLugar['local_seguro']=local['local_seguro']
                    dataLugar['nombre_propietario']=local['nombre_propietario']
                    dataLugar['apellido_propietario']=local['apellido_propietario']
                    dataLugar['descripcion'] = lugarLocal.descripcion
                    dataLugar['tipos_productos'] = list(lugarLocal.productos.values_list('nombre', flat=True))
                    dataLugar['servicios_adicionales'] = list(lugarLocal.servicios_adicionales.values_list('nombre', flat=True))
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

    @action(detail=False, url_path ='get_reseñas', methods=['post'])
    def get_reseñas(self, request):
        try:
            data = request.data
            lugar = get_or_none(Lugar, token=data['token_lugar'])
            reseñas = Reseña.getReseñasByIdLugar(lugar.id)
            for reseña in reseñas:
                fecha= reseña['fecha_creacion']
                reseña['fecha_creacion']=fecha.strftime('%Y-%m-%d %H:%M:%S')
                reseña['fecha_creacion']=str(reseña['fecha_creacion'])

            return jsonx({'status': 'success', 'reseñas': reseñas})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
        
    @action(detail=False, url_path ='new_reseña', methods=['post'])
    def new_reseña(self, request):
        try: 
            data= request.data
            if data['token_lugar'] is not None and data['token_lugar'] != '':
                lugar = get_or_none(Lugar, token=data['token_lugar'])
                token= Token.objects.get(key=request.headers['Authorization'].split('Token ')[1]) 
                reseña = Reseña()
                reseña.contenido = data['contenido']
                reseña.puntuacion_seguridad = data['puntuacion_seguridad']
                if data.get('puntuacion_atencion') is not None and data.get('puntuacion_atencion') != '':
                    reseña.puntuacion_atencion = data['puntuacion_atencion']
                if data.get('puntuacion_limpieza') is not None and data.get('puntuacion_limpieza') != '':
                    reseña.puntuacion_limpieza = data['puntuacion_limpieza']

                reseña.lugar = lugar
                reseña.user = token.user
                reseña.save()

                return jsonx({'status': 'success', 'message': 'Reseña creada con éxito.'})
            else:
                return jsonx({'status': 'error', 'message': 'El lugar no existe.'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
    
    @action(detail=False, url_path ='delete_reseña', methods=['post'])
    def delete_reseña(self, request):
        try:
            data= request.data
            reseña = get_or_none(Reseña, token=data['token_reseña'])
            reseña.delete()
            return jsonx({'status': 'success', 'message': 'Reseña eliminada con éxito.'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
    
    @action(detail=False, url_path ='edit_reseña', methods=['post'])
    def edit_reseña(self, request):
        try:
            data= request.data
            reseña = get_or_none(Reseña, token=data['token_reseña'])
            reseña.contenido = data['contenido']
            if data['puntuacion_seguridad'] is not None and data['puntuacion_seguridad'] != '':
                reseña.puntuacion_seguridad = data['puntuacion_seguridad']
            if data.get('puntuacion_atencion') is not None and data.get('puntuacion_atencion') != '':
                reseña.puntuacion_atencion = data['puntuacion_atencion']
            if data.get('puntuacion_limpieza') is not None and data.get('puntuacion_limpieza') != '':
                reseña.puntuacion_limpieza = data['puntuacion_limpieza']
                   
                
            reseña.save()

            return jsonx({'status': 'success', 'message': 'Reseña editada con éxito.'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
        

    


