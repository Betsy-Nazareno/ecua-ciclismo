from django.db import models

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.apps.backend.ruta.models import Etiqueta, Archivo
from ecuaciclismo.apps.helpers.models import ModeloBase


class Publicacion(ModeloBase):
    titulo = models.TextField()
    descripcion = models.TextField()

class ComentarioPublicacion(ModeloBase):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)

class DetalleEtiquetaPublicacion(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.PROTECT)

class DetalleArchivoPublicacion(ModeloBase):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT)
    archivo = models.ForeignKey(Archivo, on_delete=models.PROTECT)
