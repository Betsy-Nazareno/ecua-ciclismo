from django.db import transaction
from django.forms import ValidationError
from rest_framework import viewsets
from datetime import datetime
from ecuaciclismo.apps.backend.api.solicitud.SolicitudSerializer import SolicitudSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from ecuaciclismo.apps.backend.lugar.models import Lugar
from ecuaciclismo.apps.backend.solicitud.models import Solicitud
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none
from rest_framework.authtoken.models import Token
from ecuaciclismo.helpers.jsonx import jsonx

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class= SolicitudSerializer
    queryset = Solicitud.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset
    @action(detail=False, utl_path='new_solicitud_lugar', methods=['post'])
    def new_solicitud_lugar(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            solicitud = Solicitud()
            user= Token.objects.get(key=data['token']).user
            solicitud.user = user
            lugar=get_or_none(Lugar, token=data['token_lugar'])
            solicitud.lugar = lugar
            solicitud.path_Pdf=data['path_Pdf']
            solicitud.estado = 'Pendiente'
            solicitud.save()
            transaction.commit()

            return jsonx({'status': 'success', 'message': 'Solicitud de lugar creado con éxito'})
        except ValidationError as e:
            return jsonx({'status': 'error', 'message': e.message_dict})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx(False, str(e))
        
        