from django.contrib.auth.models import User
from django.db import models, connection

from ecuaciclismo.helpers.models import ModeloBase

class Bicicleta(ModeloBase):
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(null=True)
    estado = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20)
    foto_bicicleta = models.TextField()

class DetalleUsuario(ModeloBase):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    celular = models.CharField(max_length=10, null=True)
    fecha_nacimiento = models.DateField(null=True)
    genero = models.CharField(max_length=15, null=True)
    nivel = models.TextField(null=True)
    foto = models.TextField(null=True)
    admin = models.BooleanField(default=False)
    token_notificacion = models.TextField(null=True)
    peso = models.FloatField(null=True)

    def __init__(self, *args, **kwargs):
        super(DetalleUsuario, self).__init__(*args, **kwargs)

    @classmethod
    def token_notificacion_users(cls, admin):
        cursor = connection.cursor()
        sql = '''
                SELECT detalle_usuario.token_notificacion
                FROM usuario_detalleusuario AS detalle_usuario
                WHERE detalle_usuario.admin = 
            ''' + admin

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic