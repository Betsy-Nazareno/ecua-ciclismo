from django.db import models, connection
from django.contrib.auth.models import User
from ecuaciclismo.apps.backend.lugar.models import Lugar

from ecuaciclismo.helpers.models import ModeloBase

class Solicitud(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    motivo_rechazo = models.CharField(max_length=200, blank=True, null=True)
    path_Pdf = models.TextField(null=True)

    @classmethod
    def get_all(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT 
                user.first_name, 
                user.last_name,
                token.key as token_usuario,
                detalle_usuario.foto, 
                detalle_usuario.token_notificacion,
                detalle_usuario.isPropietary AS es_propietario,
                solicitud.token, solicitud.estado, 
                solicitud.fecha_creacion,
                solicitud.path_Pdf, 
                solicitud.id, 
                solicitud.motivo_rechazo
            FROM `solicitud_solicitud` AS solicitud
            LEFT JOIN `auth_user` AS user ON 
                solicitud.user_id = user.id
            LEFT JOIN `authtoken_token` AS token ON 
                solicitud.user_id = token.user_id
            LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON 
                solicitud.user_id = detalle_usuario.usuario_id
            ORDER BY 
                solicitud.fecha_creacion 
            '''
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic
    
    @classmethod
    def get_by_token(cls, token):
        cursor = connection.cursor()
        sql = '''
                SELECT user.first_name, user.last_name,token.key as token_usuario, detalle_usuario.foto, solicitud.token, solicitud.estado, solicitud.fecha_creacion,solicitud.path_Pdf, solicitud.id
                FROM `solicitud_solicitud` AS solicitud
                LEFT JOIN `auth_user` AS user ON solicitud.user_id = user.id
                LEFT JOIN `authtoken_token` AS token ON solicitud.user_id = token.user_id
                LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON solicitud.user_id = detalle_usuario.usuario_id
                WHERE solicitud.id = ''' + str(token) + '''
            '''
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class SolicitudLugar(Solicitud):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE) 

    @classmethod
    def get_by_id(cls, id):
        cursor = connection.cursor()
        sql = '''
                SELECT lugar.nombre, lugar.direccion, lugar.descripcion, lugar.id, lugar.imagen, lugar.ubicacion_id
                FROM `solicitud_solicitudlugar` AS solicitud
                LEFT JOIN `lugar_lugar` AS lugar ON solicitud.lugar_id = lugar.id
                WHERE solicitud.solicitud_ptr_id =''' + str(id)
            
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic




class SolicitudVerificado(Solicitud):
    descripcion = models.TextField()
    imagen = models.TextField()
    usuarios = models.ManyToManyField(User)

    @classmethod
    def get_Usuarios(self, id):
        cursor = connection.cursor()
        sql = '''
                SELECT user.first_name, user.last_name, detalle_usuario.foto, detalle_usuario.tipo, user.id
                FROM `solicitud_solicitudverificado_usuarios` AS solicitud_usuario
                LEFT JOIN `auth_user` AS user ON solicitud_usuario.user_id = user.id
                LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON user.id = detalle_usuario.usuario_id
                WHERE solicitud_usuario.solicitudverificado_id = ''' + str(id)
            
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic
