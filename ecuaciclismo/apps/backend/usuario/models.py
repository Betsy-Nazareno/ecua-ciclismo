from django.contrib.auth.models import User
from django.db import models, connection

from ecuaciclismo.apps.backend.ruta.models import EtiquetaRuta
from ecuaciclismo.helpers.models import ModeloBase

class Bicicleta(ModeloBase):
    marca = models.CharField(max_length=20, null=True)
    tipo = models.CharField(max_length=20, null=True)
    codigo = models.TextField(null=True)
    foto_bicicleta = models.TextField(null=True)

class DetalleUsuario(ModeloBase):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    fecha_nacimiento = models.DateField(null=True)
    genero = models.CharField(max_length=15, null=True)
    nivel = models.TextField(null=True)
    foto = models.TextField(null=True)
    admin = models.BooleanField(default=False)
    token_notificacion = models.TextField(null=True)
    peso = models.FloatField(null=True)
    bicicleta = models.OneToOneField(Bicicleta, on_delete=models.PROTECT, null=True)

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

class DetalleEtiquetaRutaUsuario(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    etiqueta = models.ForeignKey(EtiquetaRuta, on_delete=models.PROTECT)