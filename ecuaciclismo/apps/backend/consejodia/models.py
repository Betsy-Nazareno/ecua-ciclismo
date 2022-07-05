from django.db import models, connection

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.helpers.models import ModeloBase


class ConsejoDia(ModeloBase):
    informacion = models.TextField()
    imagen = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @classmethod
    def get_consejos_del_dia(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT informacion, imagen, consejo_dia.token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
            FROM consejodia_consejodia AS consejo_dia
            LEFT JOIN `auth_user` AS usuario ON consejo_dia.user_id = usuario.id
            LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON consejo_dia.user_id = detalle_usuario.usuario_id
            WHERE consejo_dia.ultimo_cambio > CURDATE()
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
                SELECT informacion, imagen, consejo_dia.token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
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
    nombre = models.TextField(null=True)
    celular = models.TextField(null=True)
    direccion = models.TextField(null=True)

    @classmethod
    def get_novedades(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT novedad.titulo, novedad.descripcion, novedad.descripcion_corta, novedad.token, novedad.nombre, novedad.celular, novedad.direccion
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
