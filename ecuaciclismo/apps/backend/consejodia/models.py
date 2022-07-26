from django.db import models, connection

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.helpers.models import ModeloBase


class ConsejoDia(ModeloBase):
    informacion = models.TextField()
    imagen = models.TextField()
    path = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @classmethod
    def get_consejos_del_dia(cls):
        cursor = connection.cursor()
        cursor.execute("SET time_zone = '-5:00';")
        sql = '''
            SELECT informacion, imagen, consejo_dia.path, consejo_dia.token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
            FROM consejodia_consejodia AS consejo_dia
            LEFT JOIN `auth_user` AS usuario ON consejo_dia.user_id = usuario.id
            LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON consejo_dia.user_id = detalle_usuario.usuario_id
            WHERE consejo_dia.ultimo_cambio >= NOW() - INTERVAL 1 DAY;
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
    def get_historico_consejos_del_dia(cls):
        cursor = connection.cursor()
        sql = '''
                SELECT informacion, imagen, consejo_dia.path, consejo_dia.token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
                FROM consejodia_consejodia AS consejo_dia
                LEFT JOIN `auth_user` AS usuario ON consejo_dia.user_id = usuario.id
                LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON consejo_dia.user_id = detalle_usuario.usuario_id
            '''

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class Novedad(ModeloBase):
    titulo = models.TextField()
    descripcion = models.TextField()
    descripcion_corta = models.TextField()
    imagen = models.TextField()
    path = models.TextField(null=True)
    nombre = models.TextField(null=True)
    celular = models.TextField(null=True)
    direccion = models.TextField(null=True)

    @classmethod
    def get_novedades(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT novedad.titulo, novedad.descripcion, novedad.descripcion_corta, novedad.imagen, novedad.path, novedad.token, novedad.nombre, novedad.celular, novedad.direccion
            FROM consejodia_novedad AS novedad
        '''

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class Reaccion(ModeloBase):
    nombre = models.TextField()

    @classmethod
    def get_reacciones(cls, consejo_dia_id, nombre_reaccion):
        cursor = connection.cursor()
        sql = '''
                SELECT reaccion.nombre, GROUP_CONCAT(reaccion_consejo.user_id) AS usuarios
                FROM consejodia_reaccion AS reaccion
                LEFT JOIN `consejodia_detallereaccionconsejo` AS reaccion_consejo ON reaccion.id = reaccion_consejo.reaccion_id
                WHERE reaccion_consejo.consejo_dia_id = %s AND reaccion.nombre LIKE %s
                GROUP BY reaccion.nombre
            '''
        nombre_reaccion = '%' + nombre_reaccion + '%'
        params = [consejo_dia_id, nombre_reaccion]
        cursor.execute(sql, params)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

    @classmethod
    def get_reacciones_publicaciones(cls, publicacion_id, nombre_reaccion):
        cursor = connection.cursor()
        sql = '''
                    SELECT reaccion.nombre, GROUP_CONCAT(reaccion_publicacion.user_id) AS usuarios
                    FROM consejodia_reaccion AS reaccion
                    LEFT JOIN `publicacion_detallereaccionpublicacion` AS reaccion_publicacion ON reaccion.id = reaccion_publicacion.reaccion_id
                    WHERE reaccion_publicacion.publicacion_id = %s AND reaccion.nombre LIKE %s
                    GROUP BY reaccion.nombre
                '''
        nombre_reaccion = '%' + nombre_reaccion + '%'
        params = [publicacion_id, nombre_reaccion]
        cursor.execute(sql, params)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

    @classmethod
    def get_all_reacciones(cls):
        cursor = connection.cursor()
        sql = '''
                SELECT reaccion.nombre
                FROM consejodia_reaccion AS reaccion
        '''
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetalleReaccionConsejo(ModeloBase):
    consejo_dia = models.ForeignKey(ConsejoDia, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reaccion = models.ForeignKey(Reaccion, on_delete=models.PROTECT)
