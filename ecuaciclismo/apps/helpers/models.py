# coding=utf-8
#django
from django.db import models

# ecuaciclismo


class ModeloBase(models.Model):
    """ Modelo base para todos los modelos del comextweb """
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_cambio = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True