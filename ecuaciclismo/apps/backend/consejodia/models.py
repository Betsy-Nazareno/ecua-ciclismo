from django.db import models

# Create your models here.
from rest_framework.authtoken.admin import User

from ecuaciclismo.apps.helpers.models import ModeloBase


class ConsejoDia(ModeloBase):
    informacion = models.TextField()
    imagen = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

