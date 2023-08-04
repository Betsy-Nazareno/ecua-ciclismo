from django.db import models
from django.contrib.auth.models import User
from ecuaciclismo.apps.backend.lugar.models import Lugar

from ecuaciclismo.helpers.models import ModeloBase

class Solicitud(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    motivo_rechazo = models.CharField(max_length=200, blank=True, null=True)
    path_Pdf = models.TextField(null=True)

class SolicitudRegistroMiembro(Solicitud):
    cedula = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=50)
    seguro_medico = models.CharField(max_length=100)
    tipo_sangre = models.CharField(max_length=50)
    contacto_emergencia = models.CharField(max_length=50)
    comprobante = models.TextField(null=True)  # LongText en MySQL
    foto_cedula = models.TextField()  # LongText en MySQL

class SolicitudLugar(Solicitud):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)


class SolicitudVerificado(Solicitud):
    descripcion = models.TextField()
    imagen = models.TextField()
    usuarios = models.ManyToManyField(User)
