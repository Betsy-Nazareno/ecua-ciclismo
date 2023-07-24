from django.contrib.auth.models import User
from django.db import models, connection

from ecuaciclismo.apps.backend.ruta.models import Archivo,Colaboracion,Ubicacion
from ecuaciclismo.helpers.models import ModeloBase

class EtiquetaAlerta(ModeloBase):
    nombre = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

class Alerta(ModeloBase):
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=100)
    fecha_fin = models.CharField(max_length=100)
    motivo_cancelacion = models.CharField(max_length=200)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    etiqueta = models.ForeignKey(EtiquetaAlerta, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ArchivoAlerta(ModeloBase):
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)

class ComentarioAlerta(ModeloBase):
    comentario = models.TextField()
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    padre= models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='respuestas')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ParticipacionAlerta(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)

class DetalleColaboracion(ModeloBase):
    colaboracion = models.ForeignKey(Colaboracion, on_delete=models.CASCADE,related_name='colaboraciones')
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)


