from django.contrib.auth.models import User
from django.db import models, connection

from ecuaciclismo.apps.backend.ruta.models import Ubicacion
from ecuaciclismo.apps.backend.local_detalles.models import Producto, ServicioAdicional

from ecuaciclismo.helpers.models import ModeloBase

class Servicio(ModeloBase):
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

class Lugar(ModeloBase):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    direccion = models.CharField(max_length=100)
    imagen = models.TextField()
    ciudad = models.CharField(max_length=100, null=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=True)
    isActived = models.BooleanField(default=0)

    @classmethod
    def get_lugares(self,activo):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    lugar.nombre AS nombre,
                    lugar.descripcion AS descripcion,
                    lugar.imagen AS imagen,
                    lugar.ubicacion_id AS ubicacion,
                    CASE
                        WHEN parqueadero.lugar_ptr_id IS NOT NULL THEN 'parqueadero'
                        WHEN local.lugar_ptr_id IS NOT NULL THEN 'local'
                        WHEN ciclovia.lugar_ptr_id IS NOT NULL THEN 'ciclovia'
                        ELSE ''
                    END AS tipo,
                    local.isVerificado AS local_seguro,
                    lugar.direccion AS direccion,
                    lugar.token AS token,
                    lugar.ciudad AS ciudad,
                    IF(local.isVerificado AND detalle_usuario.isPropietary, 1, 0) AS local_safepoint
                FROM
                    lugar_lugar AS lugar
                LEFT JOIN lugar_parqueadero AS parqueadero ON
                    lugar.id = parqueadero.lugar_ptr_id
                LEFT JOIN lugar_local AS local ON
                    lugar.id = local.lugar_ptr_id
                LEFT JOIN auth_user AS usuario ON 
                    usuario.id = local.user_id
                LEFT JOIN usuario_detalleusuario AS detalle_usuario ON
                    (detalle_usuario.usuario_id = usuario.id)
                LEFT JOIN lugar_ciclovia AS ciclovia ON
                    lugar.id = ciclovia.lugar_ptr_id
                WHERE 
                    lugar.isActived = %s
                    AND lugar.ubicacion_id IS NOT NULL
            """, [activo])
            result = cursor.fetchall()

        lugares = []
        for row in result:
            lugar_info = {
                'nombre': row[0],
                'descripcion': row[1],
                'imagen': row[2],
                'ubicacion': row[3],
                'tipo': row[4],
                'local_seguro': row[5] if row[4] == 'local' else None,
                'direccion': row[6],
                'token': row[7],
                'ciudad': row[8],
                'local_safepoint': row[9]
            }
            lugares.append(lugar_info)

        return lugares

    @classmethod
    def getTipoLugar(self,id_lugar):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    CASE
                        WHEN parqueadero.lugar_ptr_id IS NOT NULL THEN 'parqueadero'
                        WHEN local.lugar_ptr_id IS NOT NULL THEN 'local'
                        WHEN ciclovia.lugar_ptr_id IS NOT NULL THEN 'ciclovia'
                        ELSE ''
                    END AS tipo
                FROM lugar_lugar as lugar 
                LEFT JOIN lugar_parqueadero as parqueadero  ON lugar.id = parqueadero.lugar_ptr_id
                LEFT JOIN lugar_local as local  ON lugar.id = local.lugar_ptr_id
                LEFT JOIN lugar_ciclovia as ciclovia  ON lugar.id = ciclovia.lugar_ptr_id
                WHERE lugar.id = %s 
            """, [id_lugar])
            row = cursor.fetchone()

        if row:
            return row[0]
        else:
            return None
    @classmethod
    def getLugarById(self, lugar_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    lugar.id AS id,
                    lugar.nombre AS nombre,
                    lugar.descripcion AS descripcion,
                    lugar.imagen AS imagen,
                    lugar.direccion AS direccion,
                    lugar.ubicacion_id AS ubicacion,
                    CASE
                        WHEN parqueadero.lugar_ptr_id IS NOT NULL THEN 'parqueadero'
                        WHEN local.lugar_ptr_id IS NOT NULL THEN 'local'
                        WHEN ciclovia.lugar_ptr_id IS NOT NULL THEN 'ciclovia'
                        ELSE ''
                    END AS tipo,
                    lugar.ciudad AS ciudad,
                    lugar.token AS token
                FROM lugar_lugar as lugar
                LEFT JOIN lugar_parqueadero as parqueadero  ON lugar.id = parqueadero.lugar_ptr_id
                LEFT JOIN lugar_local as local  ON lugar.id = local.lugar_ptr_id
                LEFT JOIN lugar_ciclovia as ciclovia  ON lugar.id = ciclovia.lugar_ptr_id
                WHERE lugar.id = %s
            """, [lugar_id])
            row = cursor.fetchone()

        if row:
            lugar_info = {
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'imagen': row[3],
                'direccion': row[4],
                'ubicacion': row[5],
                'tipo': row[6],
                'ciudad': row[7],
                'token': row[8],
            }
            return lugar_info
        else:
            return None


class Parqueadero(Lugar):
    capacidad = models.IntegerField()
    tarifa = models.IntegerField()

    @classmethod
    def getParqueaderoById(self, lugar_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    parqueadero.capacidad AS capacidad,
                    parqueadero.tarifa AS tarifa
                FROM lugar_parqueadero as parqueadero
                WHERE parqueadero.lugar_ptr_id = %s
            """, [lugar_id])
            row = cursor.fetchone()

        if row:
            capacidad = row[0]
            tarifa = row[1]

            return {
                'capacidad': capacidad,
                'tarifa': tarifa,
            }
        else:
            return None

class Local(Lugar):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, null=True)    
    celular = models.CharField(max_length=100,null=True)
    hora_inicio = models.TimeField(null=True)
    hora_fin = models.TimeField(null=True)
    isBeneficios = models.BooleanField(default=0)
    isVerificado = models.BooleanField(default=0)
    isParqueadero= models.BooleanField(null=True)
    productos = models.ManyToManyField(Producto, related_name='locales')
    servicios_adicionales = models.ManyToManyField(ServicioAdicional, related_name='locales')
    
    @classmethod
    def getLocalById(self, lugar_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    auth_user.first_name AS nombre_propietario,
                    auth_user.last_name AS apellido_propietario,
                    local.servicio_id AS id_servicio,
                    local.celular AS celular,
                    local.hora_inicio AS hora_inicio,
                    local.hora_fin AS hora_fin,
                    local.isVerificado AS is_verificado,
                    local.isBeneficios AS isBeneficios
                FROM lugar_local as local
                INNER JOIN auth_user ON local.user_id = auth_user.id
                WHERE local.lugar_ptr_id = %s
            """, [lugar_id])
            row = cursor.fetchone()
        if row:
            nombre_propietario = row[0] 
            apellido_propietario = row[1]
            id_servicio = row[2]
            celular = row[3]
            hora_inicio = row[4]
            hora_fin = row[5]
            is_verificado = row[6]
            isBeneficios = row[7]

            return {
                'nombre_propietario': nombre_propietario,
                'apellido_propietario': apellido_propietario,
                'id_servicio': id_servicio,
                'celular': celular,
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'local_seguro': is_verificado,
                'isBeneficios': isBeneficios,
            }
        else:
            return None

class Ciclovia(Lugar):
    longitud = models.FloatField()
    @classmethod
    def getCicloviaById(self, lugar_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    ciclovia.longitud AS longitud
                FROM lugar_ciclovia as ciclovia
                WHERE ciclovia.lugar_ptr_id = %s
            """, [lugar_id])
            row = cursor.fetchone()

        if row:
            longitud = row[0]

            return {
                'longitud': longitud,
            }
        else:
            return None
        

class Reseña(ModeloBase):
    contenido = models.TextField()
    puntuacion_atencion = models.IntegerField(null=True)
    puntuacion_limpieza = models.IntegerField(null=True)
    puntuacion_seguridad = models.IntegerField()
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def getPuntuacionesByIdLugar(self, lugar_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    AVG(puntuacion_atencion) AS promedio_atencion,
                    AVG(puntuacion_limpieza) AS promedio_limpieza,
                    AVG(puntuacion_seguridad) AS promedio_seguridad
                FROM lugar_reseña as reseña
                WHERE lugar_id = %s
            """, [lugar_id])
            row = cursor.fetchone()

        if row:
            promedio_atencion = row[0]
            promedio_limpieza = row[1]
            promedio_seguridad = row[2]

            return {
                'promedio_atencion': promedio_atencion,
                'promedio_limpieza': promedio_limpieza,
                'promedio_seguridad': promedio_seguridad,
            }
        else:
            return None
        
    @classmethod
    def getReseñasByIdLugar(self, lugar_id):
        cursor=connection.cursor()
        sql='''
            SELECT usuario.first_name, usuario.last_name, detalle_usuario.foto, detalle_usuario.tipo, reseña.contenido, reseña.fecha_creacion, reseña.token, reseña.puntuacion_atencion, reseña.puntuacion_limpieza, reseña.puntuacion_seguridad, token.key
            FROM lugar_reseña as reseña
            LEFT JOIN auth_user AS usuario ON reseña.user_id = usuario.id
            LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON reseña.user_id = detalle_usuario.usuario_id
            LEFT JOIN `authtoken_token` AS token ON token.user_id = reseña.user_id
            WHERE lugar_id ='''+str(lugar_id)
        
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic
