# coding=utf-8
import os
import sys
import threading
from datetime import datetime
from io import BytesIO



# ===============================================================================
from django.db import transaction

path_project = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../../..'))
sys.path.append(path_project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecuaciclismo.settings'
# ===============================================================================

# Para que ejecute en ecuaciclismo 2022
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from ecuaciclismo.apps.backend.consejodia.models import Reaccion
from ecuaciclismo import settings

def crear_reacciones():
    reaccion = Reaccion()
    reaccion.nombre = 'encanta'
    reaccion.save()
    reaccion = Reaccion()
    reaccion.nombre = 'like'
    reaccion.save()
    reaccion = Reaccion()
    reaccion.nombre = 'fuerza'
    reaccion.save()
    reaccion = Reaccion()
    reaccion.nombre = 'apoyo'
    reaccion.save()
    reaccion = Reaccion()
    reaccion.nombre = 'ciclista'
    reaccion.save()

if __name__ == '__main__':
    crear_reacciones()