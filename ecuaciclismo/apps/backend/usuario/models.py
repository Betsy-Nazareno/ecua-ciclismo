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
    #fecha_nacimiento = models.DateField(null=True)
    edad = models.IntegerField(null=True)
    genero = models.CharField(max_length=15, null=True)
    nivel = models.TextField(null=True)
    foto = models.TextField(null=True)
    admin = models.BooleanField(default=False)
    token_notificacion = models.TextField(null=True)
    peso = models.FloatField(null=True)
    bicicleta = models.OneToOneField(Bicicleta, on_delete=models.PROTECT, null=True)
    # Nuevos atributos agregados:
    tipo = models.CharField(max_length=20, null=True, default="Miembro")
    isPropietary = models.BooleanField(default=False)
    silenciar_notificaciones = models.BooleanField(default=False)
    telefono = models.CharField(max_length=15, null=True)
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

    @classmethod
    def get_all_informacion(cls, id):
        cursor = connection.cursor()
        sql = '''
                SELECT detalle_usuario.admin, bicicleta.marca, bicicleta.tipo as tipoBicicleta, bicicleta.foto_bicicleta, bicicleta.codigo, detalle_usuario.genero, detalle_usuario.nivel, detalle_usuario.foto, detalle_usuario.peso, detalle_usuario.edad, detalle_usuario.telefono, detalle_usuario.token_notificacion,detalle_usuario.isPropietary, detalle_usuario.tipo, usuario.username, usuario.first_name, usuario.last_name, usuario.email FROM `usuario_detalleusuario` AS detalle_usuario
                LEFT JOIN `auth_user` AS usuario ON detalle_usuario.usuario_id = usuario.id
                LEFT JOIN `usuario_bicicleta` AS bicicleta ON bicicleta.id = detalle_usuario.bicicleta_id
                WHERE detalle_usuario.usuario_id = ''' + str(id)

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

    @classmethod
    def get_all_users(cls):
        cursor = connection.cursor()
        sql = '''
        SELECT detalle_usuario.admin, detalle_usuario.token AS token_usuario,detalle_usuario.isPropietary, detalle_usuario.tipo, usuario.first_name, usuario.last_name, detalle_usuario.foto, detalle_usuario.usuario_id, detalle_usuario.usuario_id FROM `usuario_detalleusuario` AS detalle_usuario
        LEFT JOIN `auth_user` AS usuario ON detalle_usuario.usuario_id = usuario.id'''

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

    @classmethod
    def get_etiqueta_usuario(cls, id):
        cursor = connection.cursor()
        sql = '''
                SELECT etiqueta.token, etiqueta.nombre
                FROM `usuario_detalleetiquetarutausuario` AS detalle_etiquetarutausuario
                LEFT JOIN `ruta_etiquetaruta` AS etiqueta ON detalle_etiquetarutausuario.etiqueta_id = etiqueta.id
                WHERE detalle_etiquetarutausuario.user_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic
        
class ContactoSeguro(ModeloBase):
 	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
 	celular = models.CharField(max_length=15, null=True)
 	nombre = models.CharField(max_length=100)
 	isUser = models.BooleanField()


class GrupoContactoSeguro(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    contacto_seguro = models.ForeignKey(ContactoSeguro, on_delete=models.CASCADE)
    @classmethod
    def get_contactos_seguros_usuario(cls, id_usuario):
        cursor = connection.cursor()
        sql = '''
            SELECT cs.id, cs.nombre, cs.celular, cs.isUser, cs.token, detalle.foto, detalle.tipo, detalle.usuario_id, detalle.admin, detalle.isPropietary
            FROM usuario_grupocontactoseguro AS gcs
            INNER JOIN usuario_contactoseguro AS cs ON gcs.contacto_seguro_id = cs.id
            LEFT JOIN usuario_detalleusuario AS detalle ON cs.user_id = detalle.usuario_id
            WHERE gcs.user_id =''' + str(id_usuario)

        cursor.execute(sql)
        column_names = [col[0] for col in cursor.description]
        contactos_seguros = []
        for row in cursor.fetchall():
            contacto_seguro = dict(zip(column_names, row))
            contactos_seguros.append(contacto_seguro)
        return contactos_seguros