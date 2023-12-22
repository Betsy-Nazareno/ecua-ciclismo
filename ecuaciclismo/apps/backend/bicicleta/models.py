from django.db import models
from django.contrib.auth.models import User

class Bicicleta(models.Model):

    tipo = models.CharField(max_length=50, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    codigo = models.CharField(max_length=50, blank=True)
  
    def __str__(self):
        return f"{self.tipo} - {self.marca} - {self.codigo}"

class ImagenBicicleta(models.Model):
    imagen_url = models.CharField(max_length=200,null=True)
    path = models.TextField(null=True)
    bicicleta = models.ForeignKey(Bicicleta, related_name='imagenes', on_delete=models.CASCADE)

class PropietarioBicicleta(models.Model):
    bicicleta = models.OneToOneField(Bicicleta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
