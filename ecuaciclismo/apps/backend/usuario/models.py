from django.contrib.auth.models import User
from django.db import models

from ecuaciclismo.helpers.models import ModeloBase

class DetalleUsuario(ModeloBase):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)

    def __init__(self, *args, **kwargs):
        super(DetalleUsuario, self).__init__(*args, **kwargs)