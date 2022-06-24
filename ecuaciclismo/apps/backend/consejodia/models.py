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
            SELECT informacion, imagen, token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
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
