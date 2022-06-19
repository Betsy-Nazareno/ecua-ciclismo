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
            SELECT id, informacion, imagen, user_id FROM `consejodia_consejodia`
        '''

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic
