from django.db import models

from ecuaciclismo.helpers.models import ModeloBase

class Producto(ModeloBase):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class ServicioAdicional(ModeloBase):
    nombre = models.CharField(max_length=250, null=False)
    
    def __str__(self):
        return self.nombre
