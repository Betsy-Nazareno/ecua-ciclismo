from rest_framework import viewsets
from rest_framework.authtoken.admin import User
from rest_framework.decorators import action

from ecuaciclismo.apps.backend.api.consejodia.serializers import ConsejoDiaSerializer
from ecuaciclismo.apps.backend.consejodia.models import ConsejoDia
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none
from rest_framework import permissions



class ConsejoDiaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsejoDiaSerializer
    queryset = ConsejoDia.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(detail=False, url_path='get_consejos_dia', methods=['get'], permission_classes=[permissions.AllowAny])
    def get_consejos_dia(self, request):
        try:
            #data = request.query_params
            data = ConsejoDia.get_consejos_del_dia()

            return jsonx({'status':'success', 'message':'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status':'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='new_consejo_dia', methods=['post'], permission_classes=[permissions.AllowAny])
    def new_consejo_dia(self, request):
        try:
            data = request.data
            consejo_dia = ConsejoDia()
            consejo_dia.informacion = data['informacion']
            consejo_dia.imagen = data['imagen'] #GESTIONAR CON API
            consejo_dia.user = get_or_none(User,id=1) #Quemado de momento
            consejo_dia.save()

            return jsonx({'status': 'success', 'message': 'Consejo del día guardado con éxito.'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
