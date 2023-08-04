from django.contrib.auth.models import User
from django.db import models, connection
from ecuaciclismo.apps.backend.ruta.models import Ubicacion

from ecuaciclismo.helpers.models import ModeloBase

class Servicio(ModeloBase):
    nombre = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

class Lugar(ModeloBase):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    direccion = models.CharField(max_length=100)
    imagen = models.TextField()
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    isActived = models.BooleanField(default=0)

    @classmethod
    def get_lugares(self,activo):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    lugar.nombre AS nombre,
                    lugar.descripcion AS descripcion,
                    lugar.imagen AS imagen,
                    ubi.nombre AS ubicacion,
                    CASE
                        WHEN parqueadero.id IS NOT NULL THEN 'parqueadero'
                        WHEN local.id IS NOT NULL THEN 'local'
                        WHEN ciclovia.id IS NOT NULL THEN 'ciclovia'
                        ELSE ''
                    END AS tipo,
                    local.isVerificado AS local_verificado
                FROM lugar 
                LEFT JOIN parqueadero  ON lugar.id = parqueadero.lugar_ptr_id
                LEFT JOIN local  ON lugar.id = local.lugar_ptr_id
                LEFT JOIN ciclovia  ON lugar.id = ciclovia.lugar_ptr_id
                INNER JOIN ruta_ubicacion ubi ON lugar.ubicacion_id = ubi.id
                WHERE lugar.isActived =""")+str(activo)
            result = cursor.fetchall()

        lugares = []
        for row in result:
            lugar_info = {
                'nombre': row[0],
                'descripcion': row[1],
                'imagen': row[2],
                'ubicacion': row[3],
                'tipo': row[4],
                'local_verificado': row[5] if row[4] == 'local' else None,
            }
            lugares.append(lugar_info)

        return lugares

    @classmethod
    def getLugarById(self, lugar_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    lugar.id AS id,
                    lugar.nombre AS nombre,
                    lugar.descripcion AS descripcion,
                    lugar.imagen AS foto,
                    lugar.direccion AS direccion,
                    CASE
                        WHEN parqueadero.id IS NOT NULL THEN 'parqueadero'
                        WHEN local.id IS NOT NULL THEN 'local'
                        WHEN ciclovia.id IS NOT NULL THEN 'ciclovia'
                        ELSE ''
                    END AS tipo
                FROM lugar 
                LEFT JOIN parqueadero  ON lugar.id = parqueadero.lugar_ptr_id
                LEFT JOIN local  ON lugar.id = local.lugar_ptr_id
                LEFT JOIN ciclovia  ON lugar.id = ciclovia.lugar_ptr_id
                WHERE lugar.id = %s
            """, [lugar_id])
            row = cursor.fetchone()

        if row:
            lugar_info = {
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'foto': row[3],
                'direccion': row[4],
                'tipo': row[5],
            }
            return lugar_info
        else:
            return None


class Parqueadero(Lugar):
    capacidad = models.IntegerField()
    tarifa = models.IntegerField()

class Local(Lugar):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)    
    celular = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    isBeneficios = models.BooleanField(default=0)
    isVerificado = models.BooleanField(default=0)

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
                    local.isVerificado AS is_verificado
                FROM local
                INNER JOIN auth_user ON local.user_id = auth_user.id
                WHERE local.id = %s
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

            return {
                'nombre_propietario': nombre_propietario,
                'apellido_propietario': apellido_propietario,
                'id_servicio': id_servicio,
                'celular': celular,
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'is_verificado': is_verificado,
            }
        else:
            return None

class Ciclovia(Lugar):
    longitud = models.FloatField()

class Reseña(ModeloBase):
    contenido = models.TextField()
    puntuacion_atencion = models.IntegerField()
    puntuacion_limpieza = models.IntegerField()
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
                FROM reseña
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
            SELECT usuario.first_name, usuario.last_name, detalle_usuario.foto, detalle_usuario.tipo, reseña.contenido, reseña.fecha_creacion
            FROM reseña
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