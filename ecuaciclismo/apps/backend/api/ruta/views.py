from django.db import transaction
from rest_framework import viewsets

from ecuaciclismo.apps.backend.api.ruta.serializers import RutaSerializer
from ecuaciclismo.apps.backend.ruta.models import Ruta, Coordenada, Ubicacion, Requisito, DetalleRequisito, \
    EtiquetaRuta, DetalleEtiquetaRuta, Archivo, DetalleArchivoRuta

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none


class RutaViewSet(viewsets.ModelViewSet):
    serializer_class = RutaSerializer
    queryset = Ruta.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    @action(detail=False, url_path='new_ruta', methods=['post'])
    def new_ruta(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            ruta = Ruta()
            ruta.nombre = data['nombre']
            ruta.descripcion = data['descripcion']
            ruta.estado = 'Disponible'
            ruta.cupos_disponibles = data['cupos_disponibles']
            ruta.lugar = data['lugar']
            ruta.fecha_inicio = data['fecha_inicio']
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                ruta.aprobado = 0
            else:
                ruta.aprobado = 1
            ruta.user = token.user
            coordenadax = Coordenada.objects.create(latitud=data['ubicacion']['coordinateX']['latitude'],longitud=data['ubicacion']['coordinateX']['longitude'])
            coordenaday = Coordenada.objects.create(latitud=data['ubicacion']['coordinateX']['latitude'],longitud=data['ubicacion']['coordinateX']['longitude'])
            ubicacion = Ubicacion.objects.create(coordenada_x=coordenadax, coordenada_y=coordenaday)
            ruta.ubicacion = ubicacion
            ruta.save()

            if data.get('requisitos'):
                for requisito_token in data['requisitos']:
                    requisito_save = get_or_none(Requisito, token=requisito_token)
                    if requisito_save is not None:
                        detalle_requisito = DetalleRequisito()
                        detalle_requisito.requisito = requisito_save
                        detalle_requisito.ruta = ruta
                        detalle_requisito.save()

            if data.get('tipoRuta'):
                for token_tipo_ruta in data['tipoRuta']:
                    etiqueta_ruta = get_or_none(EtiquetaRuta,token=token_tipo_ruta)
                    if etiqueta_ruta is not None:
                        detalle_etiqueta_ruta = DetalleEtiquetaRuta()
                        detalle_etiqueta_ruta.ruta = ruta
                        detalle_etiqueta_ruta.etiqueta = etiqueta_ruta
                        detalle_etiqueta_ruta.save()

            if data.get('fotos'):
                for elemento in data['fotos']:
                    archivo = Archivo()
                    archivo.link = elemento['link']
                    archivo.tipo = 'imagen'
                    archivo.path = elemento['path']
                    archivo.save()
                    detalle_archivo_ruta = DetalleArchivoRuta()
                    detalle_archivo_ruta.archivo = archivo
                    detalle_archivo_ruta.ruta = ruta
                    detalle_archivo_ruta.save()

            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Ruta guardado con éxito.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})