from django.db import models

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.helpers.models import ModeloBase

class Ubicacion(ModeloBase):
    latitud = models.TextField()
    longitud = models.TextField()

class Ruta(ModeloBase):
    nombre = models.TextField()
    descripcion = models.TextField()
    estado = models.TextField()
    cupos_disponibles = models.IntegerField()
    lugar = models.TextField()
    fecha_inicio = models.DateTimeField()
    aprobado = models.BooleanField()
    estimado_tiempo = models.IntegerField() #Verificar si va a guardar los numeros como minutos independientemente si lo ponen en hora
    #requisito = models.ForeignKey(Requisito,on_delete=models.PROTECT) #pensar conexion
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)

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
    descripcion = models.TextField()

class Archivo(ModeloBase):
    tipo = models.CharField(max_length=15, null=False)
    link = models.TextField(null=False)

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