from django.contrib.auth.models import User
from django.db import models, connection

from ecuaciclismo.apps.backend.ruta.models import Archivo,Colaboracion,Ubicacion
from ecuaciclismo.helpers.models import ModeloBase

class EtiquetaAlerta(ModeloBase):
    nombre = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    @classmethod
    def get_etiqueta_alerta(cls,id):
        cursor = connection.cursor()
        sql = '''
            SELECT id, nombre, value
            FROM alerta_etiquetaalerta
            WHERE alerta_etiquetaalerta.id = '''+str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class Alerta(ModeloBase):
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=100)
    fecha_fin = models.CharField(max_length=100,null=True)
    motivo_cancelacion = models.CharField(max_length=200, null=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(EtiquetaAlerta, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_alertas_de_usuario(cls, user_id):
        cursor = connection.cursor()
        
        sql = '''
            SELECT alerta.id, alerta.token, alerta.fecha_creacion, token.key as token_usuario,alerta.descripcion, alerta.estado, usuario.first_name, usuario.last_name, detalle_usuario.tipo as tipoUser, detalle_usuario.foto, etiqueta.nombre, etiqueta.value
            FROM alerta_alerta AS alerta
            LEFT JOIN `auth_user` AS usuario ON alerta.user_id = usuario.id
            LEFT JOIN `authtoken_token` AS token ON token.user_id = usuario.id
            LEFT JOIN `alerta_etiquetaalerta` as etiqueta ON alerta.etiqueta_id=etiqueta.id
            LEFT JOIN usuario_detalleusuario AS detalle_usuario ON alerta.user_id = detalle_usuario.usuario_id
            WHERE alerta.user_id = ''' + str(user_id)

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

    @classmethod
    def get_alertas_recibidas(cls, user_id):
        cursor = connection.cursor()
        sql = '''
            SELECT alerta.id, alerta.token, alerta.fecha_creacion, token.key as token_usuario, alerta.descripcion, alerta.estado, usuario.first_name, usuario.last_name, detalle_usuario.tipo as tipoUser, detalle_usuario.foto, etiqueta.nombre, etiqueta.value
            FROM alerta_alerta AS alerta
            LEFT JOIN `auth_user` AS usuario ON alerta.user_id = usuario.id
            LEFT JOIN `authtoken_token` AS token ON token.user_id = usuario.id
            LEFT JOIN `alerta_etiquetaalerta` as etiqueta ON alerta.etiqueta_id=etiqueta.id
            LEFT JOIN usuario_detalleusuario AS detalle_usuario ON alerta.user_id = detalle_usuario.usuario_id
            INNER JOIN alerta_participacionalerta AS participacion ON alerta.id = participacion.alerta_id
            WHERE participacion.user_id ='''+ str(user_id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)
        cursor.close()
        return dic
    
    @classmethod
    def get_alerta(cls, token_alerta):
        cursor = connection.cursor()
        sql = '''
                SELECT alerta.id, alerta.etiqueta_id, alerta.motivo_cancelacion,token.key as token_usuario,alerta.estado, alerta.fecha_creacion AS fecha_creacion, alerta.fecha_fin AS fecha_fin,alerta.descripcion, alerta.ubicacion_id, alerta.token, usuario.first_name, usuario.last_name, detalle_usuario.foto, detalle_usuario.tipo as tipoUser,etiqueta.nombre, etiqueta.value
                FROM alerta_alerta AS alerta
                LEFT JOIN `auth_user` AS usuario ON alerta.user_id = usuario.id
                LEFT JOIN `authtoken_token` AS token ON token.user_id = usuario.id
                LEFT JOIN `alerta_etiquetaalerta` as etiqueta ON alerta.etiqueta_id=etiqueta.id
                LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON alerta.user_id = detalle_usuario.usuario_id
                WHERE alerta.token = '%s' ''' % token_alerta

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        # print(dic)
        return dic

    @classmethod
    def update_estado(cls, alerta_id, estado, motivo):
        if motivo.strip():
            sql = "UPDATE alerta_alerta SET estado = %s, motivo_cancelacion = %s WHERE id = %s;"
            params = [estado, motivo.strip(), alerta_id]
        else:
            sql = "UPDATE alerta_alerta SET estado = %s WHERE id = %s;"
            params = [estado, alerta_id]

        with connection.cursor() as cursor:
            cursor.execute(sql, params)


class ArchivoAlerta(ModeloBase):
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)

    @classmethod
    def get_archivo_x_alerta(cls, id):
        cursor = connection.cursor()
        sql = '''
            SELECT archivo.link, archivo.tipo, archivo.path
            FROM alerta_archivoalerta AS archivo_alerta
            LEFT JOIN ruta_archivo AS archivo ON archivo_alerta.archivo_id = archivo.id
            WHERE archivo_alerta.alerta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class ComentarioAlerta(ModeloBase):
    comentario = models.TextField()
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_comentario_x_alerta(cls, id_alerta):
        cursor = connection.cursor()
        sql = '''
            SELECT usuario.username, usuario.first_name, usuario.last_name, detalle_usuario.foto,detalle_usuario.tipo, comentario_alerta.comentario, comentario_alerta.token AS token_comentario, token.key AS token_usuario, comentario_alerta.fecha_creacion
            FROM alerta_comentarioalerta AS comentario_alerta
            LEFT JOIN auth_user AS usuario ON comentario_alerta.user_id = usuario.id
            LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON comentario_alerta.user_id = detalle_usuario.usuario_id
            LEFT JOIN `authtoken_token` AS token ON token.user_id = comentario_alerta.user_id
            WHERE alerta_id ='''+str(id_alerta)

        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic
    

class ParticipacionAlerta(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    isAsistencia=  models.BooleanField(default=False)

    @classmethod
    def get_participaciones_alerta(cls, alerta_id):
        cursor = connection.cursor()
        sql = '''
            SELECT participacion_alerta.id, participacion_alerta.user_id, participacion_alerta.isAsistencia
            FROM alerta_participacionalerta AS participacion_alerta
            WHERE participacion_alerta.alerta_id ='''+ str(alerta_id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

    @classmethod
    def get_asistentes(cls, alerta_id):
        cursor = connection.cursor()
        sql = '''
        SELECT usuario.first_name, usuario.last_name, detalle_usuario.foto, detalle_usuario.tipo, usuario.username
        FROM alerta_participacionalerta AS participacion
        LEFT JOIN usuario_detalleusuario AS detalle_usuario ON participacion.user_id = detalle_usuario.usuario_id
        INNER JOIN auth_user AS usuario ON participacion.user_id = usuario.id
        WHERE participacion.alerta_id = %s AND participacion.isAsistencia = 1
        '''

        cursor.execute(sql, (alerta_id,))
        asistentes = []
        resultados = cursor.fetchall()
        for row in resultados:
            usuario_data = dict(zip([col[0] for col in cursor.description], row))
            asistentes.append(usuario_data)
        cursor.close()
        return asistentes


class DetalleColaboracion(ModeloBase):
    colaboracion = models.ForeignKey(Colaboracion, on_delete=models.CASCADE,related_name='colaboraciones')
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)

    @classmethod
    def get_colaboracion_x_alerta(cls, id):
        cursor = connection.cursor()
        sql = '''
                    SELECT colaboracion.token, colaboracion.nombre
                    FROM `alerta_detallecolaboracion` AS detalle_colaboracion
                    LEFT JOIN `ruta_colaboracion` AS colaboracion ON detalle_colaboracion.colaboracion_id = colaboracion.id
                    WHERE detalle_colaboracion.alerta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic
