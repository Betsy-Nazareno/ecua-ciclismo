from django.db import models, connection

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.apps.backend.consejodia.models import Reaccion
from ecuaciclismo.apps.backend.ruta.models import Archivo
from ecuaciclismo.helpers.models import ModeloBase

class EtiquetaPublicacion(ModeloBase):
    nombre = models.TextField()
    value = models.TextField()

class Publicacion(ModeloBase):
    titulo = models.TextField()
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @classmethod
    def get_publicaciones(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT publicacion.id, publicacion.fecha_creacion, publicacion.ultimo_cambio, titulo, descripcion, publicacion.token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
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

    @classmethod
    def get_publicacion(cls, token_publicacion):
        cursor = connection.cursor()
        sql = '''
                SELECT publicacion.id, publicacion.fecha_creacion, publicacion.ultimo_cambio, titulo, descripcion, publicacion.token, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto
                FROM publicacion_publicacion AS publicacion
                LEFT JOIN `auth_user` AS usuario ON publicacion.user_id = usuario.id
                LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON publicacion.user_id = detalle_usuario.usuario_id
                WHERE publicacion.token = ''' + "\'" + str(token_publicacion) + "\'"

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        # print(dic)
        return dic

class ComentarioPublicacion(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)
    comentario = models.TextField(null=False)

    @classmethod
    def get_comentario_x_publicacion(cls, id):
        cursor = connection.cursor()
        sql = '''
            SELECT usuario.username, usuario.first_name, usuario.last_name, detalle_usuario.foto, comentario_publicacion.comentario, comentario_publicacion.token AS token_comentario 
            FROM publicacion_comentariopublicacion AS comentario_publicacion 
            LEFT JOIN auth_user AS usuario ON comentario_publicacion.user_id = usuario.id
            LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON comentario_publicacion.user_id = detalle_usuario.usuario_id
            WHERE publicacion_id = ''' + str(id)

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetalleEtiquetaPublicacion(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)
    etiqueta = models.ForeignKey(EtiquetaPublicacion, on_delete=models.PROTECT)

    @classmethod
    def get_etiqueta_x_publicacion(cls, id):
        cursor = connection.cursor()
        sql = '''
            SELECT etiqueta.nombre, etiqueta.value
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

    @classmethod
    def get_archivo_x_publicacion(cls, id):
        cursor = connection.cursor()
        sql = '''
        SELECT archivo.link, archivo.tipo
        FROM publicacion_detallearchivopublicacion AS archivo_publicacion
        LEFT JOIN ruta_archivo AS archivo ON archivo_publicacion.archivo_id = archivo.id
        WHERE archivo_publicacion.publicacion_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetalleReaccionPublicacion(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reaccion = models.ForeignKey(Reaccion, on_delete=models.PROTECT)
