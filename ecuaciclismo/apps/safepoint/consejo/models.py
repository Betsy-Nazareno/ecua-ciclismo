from django.db import models

class Consejo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50)  # Iconos de Ionicons

    class Meta:
        db_table = 'consejos_negocios'  # Nombre correcto de la tabla en la base de datos

    def __str__(self):
        return self.nombre

class Tip(models.Model):
    id = models.AutoField(primary_key=True)
    consejo = models.ForeignKey(Consejo, related_name='tips', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    detalle = models.TextField()
    imagen = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'tip_consejo'  # Nombre correcto de la tabla en la base de datos

    def __str__(self):
        return self.titulo
