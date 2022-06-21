from django.contrib.auth.models import User
from django.db import models

from ecuaciclismo.helpers.models import ModeloBase

class Bicicleta(ModeloBase):
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(null=True)
    estado = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20)
    foto_bicicleta = models.TextField()

class DetalleUsuario(ModeloBase):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    celular = models.CharField(max_length=10, null=True)
    fecha_nacimiento = models.DateField(null=True)
    genero = models.CharField(max_length=15, null=True)
    nivel = models.IntegerField(default=0)
    foto = models.TextField(null=True)
    admin = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(DetalleUsuario, self).__init__(*args, **kwargs)

class DetalleBicicleta(ModeloBase):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.PROTECT)