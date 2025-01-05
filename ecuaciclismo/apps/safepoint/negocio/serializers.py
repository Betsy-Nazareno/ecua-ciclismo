from collections import OrderedDict
import uuid

from rest_framework import serializers, status, validators, exceptions

from django.db.models import Q
from django.contrib.auth.models import User

from ecuaciclismo.apps.backend.lugar.models import Local, Servicio
from ecuaciclismo.apps.backend.solicitud.models import SolicitudLugar
from ecuaciclismo.apps.backend.ruta.models import Coordenada, Ubicacion
from ecuaciclismo.apps.backend.logs.models import Log
from ecuaciclismo.apps.backend.local_detalles.models import Producto, ServicioAdicional, EstadisticaCiclistaLocal


class CoordenadaNegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenada
        fields = (
            'id',
            'latitud',
            'longitud'
        )

      
class UbicacionNegocioSerializer(serializers.ModelSerializer):
    coordenada_x = CoordenadaNegocioSerializer()
    coordenada_y = CoordenadaNegocioSerializer()
    
    class Meta:
        model = Ubicacion
        fields = (
            'id',
            'coordenada_x',
            'coordenada_y'
        )


class NegocioSerializer(serializers.ModelSerializer):
    ubicacion = UbicacionNegocioSerializer()
    imagen = serializers.CharField(required=False, allow_blank=True)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    debe_enviar_solicitud = serializers.SerializerMethodField()
    
    class Meta:
        model = Local
        fields = (
            'id',
            'nombre',
            'servicio',
            'imagen',
            'hora_inicio',
            'hora_fin',
            'descripcion',
            'direccion',
            'ubicacion',
            'productos',
            'servicios_adicionales',
            'debe_enviar_solicitud'
        )
        extra_kwargs = {
            'direccion': { 'required': False, 'allow_blank': True },
            'productos': { 'required': False, 'allow_empty': True },
            'servicios_adicionales': { 'required': False, 'allow_empty': True }
        }
        
    def get_debe_enviar_solicitud(self, obj):
        solicitud: SolicitudLugar = SolicitudLugar.objects.filter(lugar=obj)\
            .order_by("-fecha_creacion").first()
        if not solicitud:
            return True
        if solicitud.estado == "Aprobada" or solicitud.estado == "Pendiente":
            return False
        return solicitud.estado == "Rechazada"

    def update(self, instance, validated_data: OrderedDict):
        ubicacion_data = validated_data.pop('ubicacion')
        productos_data = validated_data.pop('productos')
        servicios_adicionales_data = validated_data.pop('servicios_adicionales')
        
        negocio: Local = super().update(instance, validated_data)
        negocio.ubicacion = self._actualizar_ubicacion(negocio.ubicacion, ubicacion_data)
        negocio.productos.set(productos_data)
        negocio.servicios_adicionales.set(servicios_adicionales_data)
        
        negocio.save()
        
        return negocio
        
    def _actualizar_ubicacion(self, ubicacion: Ubicacion, data: OrderedDict):
        if not ubicacion:
            coordenada_x = Coordenada(**data['coordenada_x'])
            coordenada_x.save()
            coordenada_y = Coordenada(**data['coordenada_y'])
            coordenada_y.save()
            
            ubicacion_negocio = Ubicacion(coordenada_x=coordenada_x,coordenada_y=coordenada_y)
            ubicacion_negocio.save()
            
            return ubicacion_negocio
        
        Coordenada.objects.filter(id=ubicacion.coordenada_x.id).update(**data['coordenada_x'])
        Coordenada.objects.filter(id=ubicacion.coordenada_y.id).update(**data['coordenada_y'])            
        ubicacion.refresh_from_db()
        
        return ubicacion

class EstadoNegocioSerializer(serializers.ModelSerializer):
    activo = serializers.BooleanField(source='isActived')
    es_verificado = serializers.BooleanField(source='isVerificado')
    
    class Meta:
        model = Local
        fields = (
            'activo',
            'es_verificado'
        )

class SolicitudNegocioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SolicitudLugar
        fields = "__all__"


class SolicitudNegocioCreacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SolicitudLugar
        exclude = (
            'token',
            'user'
        )
        read_only_fields = (
            'id',
            'estado',
            'motivo_rechazo',
            'path_Pdf',
            'fecha_creacion',
            'ultimo_cambio'
        )
        
    def create(self, validated_data):
        usuario = self.context.get('request').user
        
        solicitud: SolicitudLugar = self._obtener_ultima_solicitud(usuario, validated_data['lugar'])
        if solicitud:
            if solicitud.estado == "Pendiente":
                raise exceptions.APIException(
                    detail= { 'message': 'Ya existe una solicitud de verificacion para este negocio' },
                    code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            elif solicitud.estado == "Aprobada":
                raise exceptions.APIException(
                    detail= { 'message': 'Este negocio ya tiene una solicitud aprobada' },
                    code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            
        solicitud = SolicitudLugar(
            user=usuario,
            lugar=validated_data['lugar'],
            estado='Pendiente',
        )
        solicitud.save()
        return solicitud
        
    def _obtener_ultima_solicitud(self, usuario, negocio):
        return SolicitudLugar.objects\
            .filter(lugar=negocio)\
            .filter(user=usuario)\
            .order_by("-fecha_creacion")\
            .first()


class ServicioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Servicio
        fields = (
            'id',
            'nombre'
        )

class ProductosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre'
        )


class ServiciosAdicionalesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServicioAdicional
        fields = (
            'id',
            'nombre'
        )

class EstadisticasNegocioMesSerializer(serializers.Serializer):
    mes = serializers.SerializerMethodField()
    vistas = serializers.IntegerField(read_only=True)
    
    MESES = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 
        8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    
    def get_mes(self, obj):
        return self.MESES[obj['mes']]
    
    @classmethod
    def obtener_estadisticas_por_mes(cls, data_list: list):
        estadisticas = {
            'Enero': 0, 'Febrero': 0, 'Marzo': 0, 'Abril': 0, 'Mayo': 0,
            'Junio': 0, 'Julio': 0, 'Agosto': 0, 'Septiembre': 0, 'Octubre': 0,
            'Noviembre': 0, 'Diciembre': 0,
        }
        
        for data in data_list:
            estadisticas[data["mes"]] = data["vistas"]
        return estadisticas
        
class EstadisticasNegocioDiasSerializer(serializers.Serializer):
    dia = serializers.SerializerMethodField()
    vistas = serializers.IntegerField(read_only=True)
    
    DIAS = {
        1: "Domingo", 2: "Lunes", 3: "Martes", 4: "Miercoles", 5: "Jueves", 6: "Viernes", 7: "Sabado"
    }
    
    def get_dia(self, obj):
        return self.DIAS[obj['dia']]
    
    @classmethod
    def obtener_estadisticas_por_dia(cls, data_list: list):
        estadisticas = {
            "Domingo": 0, "Lunes": 0, "Martes": 0, "Miercoles": 0, 
            "Jueves": 0, "Viernes": 0, "Sabado": 0
        }
        
        for data in data_list:
            estadisticas[data["dia"]] = data["vistas"]
        return estadisticas

class EstadisticasActualizarVistaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EstadisticaCiclistaLocal
        fields = (
            'local',
        )
    
    def create(self, validated_data):
        ciclista: User = self.context.get('request').user
        if not ciclista:
            return exceptions.APIException("Usuario no encontrado")
        
        estadistica = EstadisticaCiclistaLocal(
            usuario=ciclista, 
            local=validated_data['local'],
            tipo=EstadisticaCiclistaLocal.TipoEstadistica.VISTA_MAPA_ECUACICLISMO
        )
        
        estadistica.save()
        return estadistica
    
class AgregarRegistroAvisoNegocio(serializers.ModelSerializer):
    descripcion = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Log
        fields = (
            'descripcion',
        )
    
    def create(self, validated_data):
        usuario: User = self.context.get('request').user
        descripcion = validated_data.get("descripcion", "Aviso al 911")
        
        log = Log(
            uuidLog=uuid.uuid4(),
            usuario=usuario,
            tipo_evento="Safepoint - Registro de aviso",
            descripcion_evento = descripcion
        )
        
        log.save()
        return log

class NegocioInfoSerializer(serializers.ModelSerializer):
    ubicacion = UbicacionNegocioSerializer()
    imagen = serializers.CharField(required=False, allow_blank=True)
    descripcion = serializers.CharField(required=False)
    
    class Meta:
        model = Local
        fields = (
            'id',
            'nombre',
            'direccion',
            'ubicacion',
            'imagen',
            'descripcion',
            'hora_inicio',
            'hora_fin',
            'productos',
            'servicios_adicionales',
            'servicio',
        )
