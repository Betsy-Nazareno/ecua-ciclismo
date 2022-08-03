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
    cupos_disponibles = models.IntegerField()
    lugar = models.TextField()
    fecha_inicio = models.DateTimeField()
    aprobado = models.BooleanField()
    estimado_tiempo = models.IntegerField(null=True) #Verificar si va a guardar los numeros como minutos independientemente si lo ponen en hora
    #requisito = models.ForeignKey(Requisito,on_delete=models.PROTECT) #pensar conexion
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @classmethod
    def get_rutas(cls):
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

class InscripcionRuta(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    # material_colaboracion = models.ForeignKey(MaterialColaboracion, on_delete=models.PROTECT) #pensar como implementar

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

class DetalleArchivoRuta(ModeloBase):
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    archivo = models.ForeignKey(Archivo, on_delete=models.PROTECT)

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
