from django.db import models
from django.contrib.auth.models import User
from ecuaciclismo.apps.backend.lugar.models import Local
from ecuaciclismo.apps.backend.ruta.models import Ruta

class ReservaRuta(models.Model):
    # Foreign Keys
    id_ruta = models.ForeignKey(
        Ruta, on_delete=models.CASCADE, db_column='ruta_id'
    )
    id_local = models.ForeignKey(
        Local, on_delete=models.CASCADE, db_column='local_id'
    )
    id_usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='usuario_id'
    )

    # Campos adicionales
    comentarios = models.TextField(blank=True, null=True)
    horas = models.FloatField(blank=True, null=True)
    kilocalorias = models.FloatField(blank=True, null=True)
    kilometros = models.FloatField(blank=True, null=True)
    velocidad = models.FloatField(blank=True, null=True)

    # Campos automáticos
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    ultimo_cambio = models.DateTimeField(auto_now=True, db_column='ultimo_cambio')

    # Configuración adicional
    class Meta:
        db_table = 'reserva_ruta'
        managed = False

    def __str__(self):
        return f'Reserva de {self.id_usuario} en la ruta {self.id_ruta}'
