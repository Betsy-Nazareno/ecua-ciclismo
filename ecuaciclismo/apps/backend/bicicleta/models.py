from django.db import models
from django.contrib.auth.models import User

class Bicicleta(models.Model):

    modelo = models.CharField(max_length=500, blank=True)
    marca = models.CharField(max_length=500, blank=True)
    codigo = models.CharField(max_length=500, blank=True)
    modalidad = models.CharField(max_length=500, blank=True)
    n_serie= models.CharField(max_length=500, blank=True)
    tienda_origen = models.CharField(max_length=500, blank=True)
    factura = models.CharField(max_length=500, blank=True)
    color = models.CharField(max_length=500, blank=True)
    def __str__(self):
        return f"{self.modelo} - {self.marca} - {self.codigo} - {self.modalidad} - {self.n_serie} - {self.tienda_origen} - {self.factura} - {self.color}"

class ImagenBicicleta(models.Model):
    imagen_url = models.CharField(max_length=200,null=True)
    path = models.TextField(null=True)
    bicicleta = models.ForeignKey(Bicicleta, related_name='imagenes', on_delete=models.CASCADE)

class PropietarioBicicleta(models.Model):
    bicicleta = models.OneToOneField(Bicicleta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
