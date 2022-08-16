from django.db import models, connection

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.helpers.models import ModeloBase

class Coordenada(ModeloBase):
    latitud = models.TextField()
    longitud = models.TextField()

class Ubicacion(ModeloBase):
    coordenada_x = models.ForeignKey(Coordenada, related_name='x_coordenada', on_delete=models.PROTECT)
    coordenada_y = models.ForeignKey(Coordenada, related_name='y_coordenada', on_delete=models.PROTECT)

class Ruta(ModeloBase):
    nombre = models.TextField()
    descripcion = models.TextField()
    estado = models.TextField()
    cupos_disponibles = models.IntegerField(null=True)
    lugar = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    aprobado = models.BooleanField()
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cancelada = models.BooleanField(default=0)
    motivo_cancelacion = models.TextField(null=True, default=None)
    finalizado = models.BooleanField(default=0)

    @classmethod
    def get_rutas(cls,admin):
        cursor = connection.cursor()
        cursor.execute("SET time_zone = '-5:00';")
        sql = '''
                SELECT ruta.finalizado, ruta.ubicacion_id, ruta.cupos_disponibles, IF(ruta.fecha_fin <= NOW(), TRUE, FALSE) AS estado_finalizado, IF(NOW() >= ruta.fecha_inicio AND NOW() < ruta.fecha_fin, TRUE, FALSE) AS estado_en_curso, IF(ruta.fecha_inicio > NOW(), TRUE, FALSE) AS estado_no_iniciada, ruta.id, ruta.token,  ruta.fecha_creacion, ruta.ultimo_cambio, ruta.fecha_inicio, ruta.fecha_fin, ruta.nombre, ruta.descripcion, ruta.estado, ruta.lugar, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto, token.key AS token_usuario, ruta.aprobado, ruta.cancelada, ruta.motivo_cancelacion
                FROM ruta_ruta AS ruta
                LEFT JOIN `auth_user` AS usuario ON ruta.user_id = usuario.id
                LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON ruta.user_id = detalle_usuario.usuario_id
                LEFT JOIN `authtoken_token` AS token ON token.user_id = ruta.user_id
            '''
        if admin == 0:
            sql = sql + " WHERE aprobado = 1"
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

    @classmethod
    def get_ruta(cls, token_ruta):
        cursor = connection.cursor()
        cursor.execute("SET time_zone = '-5:00';")
        sql = '''
                    SELECT ruta.finalizado, ruta.ubicacion_id, ruta.cupos_disponibles, IF(ruta.fecha_fin <= NOW(), TRUE, FALSE) AS estado_finalizado, IF(NOW() >= ruta.fecha_inicio AND NOW() < ruta.fecha_fin, TRUE, FALSE) AS estado_en_curso, IF(ruta.fecha_inicio > NOW(), TRUE, FALSE) AS estado_no_iniciada, ruta.id, ruta.token, ruta.fecha_creacion, ruta.ultimo_cambio, ruta.fecha_inicio, ruta.fecha_fin, ruta.nombre, ruta.descripcion, ruta.estado, ruta.lugar, usuario.username, usuario.email, usuario.first_name, usuario.last_name, detalle_usuario.foto, token.key AS token_usuario, ruta.aprobado, ruta.cancelada, ruta.motivo_cancelacion
                    FROM ruta_ruta AS ruta
                    LEFT JOIN `auth_user` AS usuario ON ruta.user_id = usuario.id
                    LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON ruta.user_id = detalle_usuario.usuario_id
                    LEFT JOIN `authtoken_token` AS token ON token.user_id = ruta.user_id
                    WHERE ruta.token = ''' + "\'" + str(token_ruta) + "\'"
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class InscripcionRuta(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    safe = models.BooleanField(null=True)
    finalizado = models.BooleanField(default=0)
    # material_colaboracion = models.ForeignKey(MaterialColaboracion, on_delete=models.PROTECT) #pensar como implementar

    @classmethod
    def get_participantes(cls, id):
        cursor = connection.cursor()
        sql = '''
                    SELECT usuario.id, usuario.username, usuario.first_name, usuario.last_name, detalle_usuario.foto, inscripcion_ruta.safe
                    FROM `ruta_inscripcionruta` AS inscripcion_ruta
                    LEFT JOIN `auth_user` AS usuario ON inscripcion_ruta.user_id = usuario.id
                    LEFT JOIN `usuario_detalleusuario` AS detalle_usuario ON inscripcion_ruta.user_id = detalle_usuario.usuario_id
                    LEFT JOIN `authtoken_token` AS token ON token.user_id = inscripcion_ruta.user_id
                    WHERE inscripcion_ruta.ruta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

    @classmethod
    def get_not_response(cls, id):
        cursor = connection.cursor()
        cursor.execute("SET time_zone = '-5:00';")
        sql = '''
                SELECT ruta.nombre, ruta.token AS token_ruta FROM `ruta_inscripcionruta` AS inscripcion_ruta 
                LEFT JOIN `ruta_ruta` AS ruta ON ruta.id = inscripcion_ruta.ruta_id
                WHERE inscripcion_ruta.safe IS NULL AND (ruta.fecha_fin <= NOW() OR ruta.finalizado = 1) AND inscripcion_ruta.finalizado = 1 AND inscripcion_ruta.user_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class ComentarioRuta(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    comentario_texto = models.TextField()

class EtiquetaRuta(ModeloBase):
    nombre = models.TextField()

    @classmethod
    def get_tipos_rutas(cls):
        cursor = connection.cursor()
        sql = '''
                SELECT token, nombre FROM ruta_etiquetaruta
            '''
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class Archivo(ModeloBase):
    tipo = models.CharField(max_length=15, null=False)
    link = models.TextField(null=False)
    path = models.TextField(null=True)

class DetalleEtiquetaRuta(ModeloBase):
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    etiqueta = models.ForeignKey(EtiquetaRuta, on_delete=models.PROTECT)

    @classmethod
    def get_tiporuta_x_ruta(cls, id):
        cursor = connection.cursor()
        sql = '''
                SELECT etiqueta.token, etiqueta.nombre
                FROM `ruta_detalleetiquetaruta` AS detalle_etiquetaruta
                LEFT JOIN `ruta_etiquetaruta` AS etiqueta ON detalle_etiquetaruta.etiqueta_id = etiqueta.id
                WHERE detalle_etiquetaruta.ruta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetalleArchivoRuta(ModeloBase):
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    archivo = models.ForeignKey(Archivo, on_delete=models.PROTECT)

    @classmethod
    def get_archivo_x_ruta(cls, id):
        cursor = connection.cursor()
        sql = '''
            SELECT archivo.link, archivo.tipo, archivo.path
            FROM ruta_detallearchivoruta AS archivo_ruta
            LEFT JOIN ruta_archivo AS archivo ON archivo_ruta.archivo_id = archivo.id
            WHERE archivo_ruta.ruta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

#Segunda parte
class RastreoRuta(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    kilometros_avanzados = models.DecimalField(decimal_places=2, max_digits=10)
    kilometros_acumulados = models.DecimalField(decimal_places=2, max_digits=10)
    tiempo_recorrido = models.IntegerField() #Tiempo en minutos guardar
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)

class Requisito(ModeloBase):
    nombre = models.TextField()

    @classmethod
    def get_requisitos(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT token, nombre FROM ruta_requisito
        '''
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetalleRequisito(ModeloBase):
    requisito = models.ForeignKey(Requisito, on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)

    @classmethod
    def get_requisito_x_ruta(cls, id):
        cursor = connection.cursor()
        sql = '''
                SELECT requisito.token, requisito.nombre
                FROM `ruta_detallerequisito` AS detalle_requisito
                LEFT JOIN `ruta_requisito` AS requisito ON detalle_requisito.requisito_id = requisito.id
                WHERE detalle_requisito.ruta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class Colaboracion(ModeloBase):
    nombre = models.TextField()

    @classmethod
    def get_colaboraciones(cls):
        cursor = connection.cursor()
        sql = '''
            SELECT token, nombre FROM ruta_colaboracion
        '''
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetalleColaboracion(ModeloBase):
    colaboracion = models.ForeignKey(Colaboracion, on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)

    @classmethod
    def get_colaboracion_x_ruta(cls, id):
        cursor = connection.cursor()
        sql = '''
                    SELECT colaboracion.token, colaboracion.nombre
                    FROM `ruta_detallecolaboracion` AS detalle_colaboracion
                    LEFT JOIN `ruta_colaboracion` AS colaboracion ON detalle_colaboracion.colaboracion_id = colaboracion.id
                    WHERE detalle_colaboracion.ruta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetalleColaboracionInscripcion(ModeloBase):
    colaboracion = models.ForeignKey(Colaboracion, on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class GrupoEncuentro(ModeloBase):
    nombre = models.TextField()

    @classmethod
    def get_grupos_encuentro(cls):
        cursor = connection.cursor()
        sql = '''
                SELECT token, nombre FROM ruta_grupoencuentro
            '''
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic

class DetallePuntoEncuentro(ModeloBase):
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    grupo_encuentro = models.ForeignKey(GrupoEncuentro, on_delete=models.PROTECT)
    lugar = models.TextField()

    @classmethod
    def get_puntosencuentros(cls, id):
        cursor = connection.cursor()
        sql = '''
                SELECT punto_encuentro.lugar, grupo_encuentro.nombre, grupo_encuentro.token
                FROM ruta_detallepuntoencuentro AS punto_encuentro
                LEFT JOIN ruta_grupoencuentro AS grupo_encuentro ON punto_encuentro.grupo_encuentro_id = grupo_encuentro.id
                WHERE punto_encuentro.ruta_id = ''' + str(id)
        cursor.execute(sql)
        dic = []
        detalles = cursor.fetchall()
        for row in detalles:
            diccionario = dict(zip([col[0] for col in cursor.description], row))
            dic.append(diccionario)

        cursor.close()
        return dic