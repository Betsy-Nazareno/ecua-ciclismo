from rest_framework import viewsets
from rest_framework.decorators import action

from ecuaciclismo.apps.backend.api.consejodia.serializers import ConsejoDiaSerializer
from ecuaciclismo.apps.backend.consejodia.models import ConsejoDia
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError


class ConsejoDiaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsejoDiaSerializer
    queryset = ConsejoDia.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(detail=False, url_path='get_consejos_dia', methods=['get'])
    def get_consejos_dia(self, request):
        try:
            #data = request.query_params
            data = ConsejoDiaSerializer(ConsejoDia.objects.all())

            return jsonx({'status':'success', 'message':'Información obtenida', 'data': data})
        except ApplicationError as msg:
            return jsonx({'status':'error', 'message': str(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})
