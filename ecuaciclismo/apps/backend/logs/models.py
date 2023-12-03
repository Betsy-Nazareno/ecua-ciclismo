from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    uuidLog = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=50)
    descripcion_evento = models.TextField()

    def __str__(self):
        return f"{self.uuidLog} - {self.tipo_evento} - {self.usuario}"