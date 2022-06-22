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

# Para que ejecute en CWA 2022
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from ecuaciclismo.apps.backend.consejodia.models import ConsejoDia
from ecuaciclismo import settings

def eliminar_consejos_del_dia():
    consejos_dia = ConsejoDia.objects.all()
    for consejo_dia in consejos_dia:
        consejo_dia.delete()

if __name__ == '__main__':
    eliminar_consejos_del_dia()
