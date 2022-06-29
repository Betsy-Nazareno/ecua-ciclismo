from django.db import models, connection

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.apps.backend.ruta.models import Archivo
from ecuaciclismo.helpers.models import ModeloBase

class EtiquetaPublicacion(ModeloBase):
    nombre = models.TextField()
    descripcion = models.TextField()

class Publicacion(ModeloBase):
    titulo = models.TextField()
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @classmethod
    def get_publicaciones(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT publicacion.id, titulo, descripcion, publicacion.token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
            FROM publicacion_publicacion AS publicacion
            LEFT JOIN `auth_user` AS usuario ON publicacion.user_id = usuario.id
            LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON publicacion.user_id = detalle_usuario.usuario_id
        '''

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        #print(dic)
        return dic

class ComentarioPublicacion(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)

class DetalleEtiquetaPublicacion(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)
    etiqueta = models.ForeignKey(EtiquetaPublicacion, on_delete=models.PROTECT)

    @classmethod
    def get_etiqueta_x_publicacion(cls, id):
        cursor = connection.cursor()
        sql = '''
            SELECT etiqueta.nombre, etiqueta.token, etiqueta.descripcion
            FROM `publicacion_detalleetiquetapublicacion` AS etiqueta_publicacion
            LEFT JOIN `publicacion_etiquetapublicacion` AS etiqueta ON etiqueta_publicacion.etiqueta_id = etiqueta.id
            WHERE etiqueta_publicacion.publicacion_id = '''+str(id)

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        # print(dic)
        return dic

class DetalleArchivoPublicacion(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)
    archivo = models.ForeignKey(Archivo, on_delete=models.PROTECT)
