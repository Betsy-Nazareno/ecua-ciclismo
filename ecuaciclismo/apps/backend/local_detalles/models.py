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

class EstadisticaCiclistaLocal(ModeloBase):
    
    class TipoEstadistica(models.TextChoices):
        VISTA_MAPA_ECUACICLISMO = "VISTA_MAPA"
    
    usuario = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    local = models.ForeignKey("lugar.Local", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=TipoEstadistica.choices, default=TipoEstadistica.VISTA_MAPA_ECUACICLISMO)
