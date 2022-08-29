import json
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from ecuaciclismo.apps.backend.api.usuario.serializers import DetalleUsuarioSerializer, \
    UsuarioRecuperarClaveSerializer
from ecuaciclismo.apps.backend.ruta.models import InscripcionRuta, DetalleArchivoRuta, Archivo, EtiquetaRuta
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario, Bicicleta, DetalleEtiquetaRutaUsuario
from ecuaciclismo.base.models import RegistroCambiarClave
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import ApplicationError, get_or_none

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class UsuarioViewSet(viewsets.ModelViewSet):
    from ecuaciclismo.apps.backend.api.usuario.serializers import UsuarioSerializer

    serializer_class = UsuarioSerializer
    queryset = User.objects.all()
    # lookup_field = 'username'

    @action(detail=False, url_path='actualizar_password', methods=['post'])
    def actualizar_password(self, request):
        transaction.set_autocommit(False)
        try:
            usuario = request.user
            data = request.data.get('user')
            dict_data = DetalleUsuario.actualizar_password(usuario=usuario,datos=data)
            transaction.commit()
            return jsonx(dict_data)

        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='crear_usuario', methods=['post'], permission_classes=[AllowAny])
    def crear_usuario(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            from django.contrib.auth.models import User
            user = User.objects.create_user(username=data['usuario'],
                                            email=data['email'],
                                            password=data['password'],
                                            first_name=data['nombre'],
                                            last_name=data['apellido']) #username, email, password obligatorio en el form
            user.save()
            detalle_usuario = DetalleUsuario()
            detalle_usuario.usuario = user
            if request.data.get('foto'):
                detalle_usuario.foto = data['foto']
            if request.data.get('genero'):
                detalle_usuario.genero = data['genero']
            if request.data.get('token_notificacion'):
                detalle_usuario.token_notificacion = data['token_notificacion']
            detalle_usuario.save()
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Se ha creado el usuario con éxito.'})

        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='token_notificacion_users', methods=['get'])
    def token_notificacion_users(self, request):
        try:
            data = DetalleUsuario.token_notificacion_users(admin='0')

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})

        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='token_notificacion_admins', methods=['get'])
    def token_notificacion_admins(self, request):
        try:
            data = DetalleUsuario.token_notificacion_users(admin='1')

            return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})

        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    # @action(detail=False, url_path='get_detalle_usuario', methods=['get'])
    # def get_detalle_usuario(self, request):
    #     try:
    #         data = DetalleUsuario.token_notificacion_users(admin='1')
    #
    #         return jsonx({'status': 'success', 'message': 'Información obtenida', 'data': data})
    #
    #     except ApplicationError as msg:
    #         transaction.rollback()
    #         return jsonx({'status': 'error', 'message': str(msg)})
    #     except ValidationError as msg:
    #         transaction.rollback()
    #         return jsonx({'status': 'error', 'message': list(msg)})
    #     except Exception as e:
    #         transaction.rollback()
    #         return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='editar_usuario', methods=['post'])
    def editar_usuario(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            from django.contrib.auth.models import User
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            user = token.user
            user.username = data['usuario']
            user.email = data['email']
            user.first_name = data['nombre']
            user.last_name = data['apellido']
            user.save()
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            detalle_usuario.foto = data['foto']
            detalle_usuario.genero = data['genero']
            detalle_usuario.edad = data['edad']
            detalle_usuario.nivel = data['nivel']
            detalle_usuario.peso = data['peso']
            if detalle_usuario.bicicleta is None:
                bicicleta = Bicicleta()
            else:
                bicicleta = Bicicleta.objects.get(id=detalle_usuario.bicicleta_id)
            bicicleta.marca = data['marca']
            bicicleta.tipo = data['tipo']
            bicicleta.codigo = data['codigo']
            bicicleta.foto_bicicleta = data['foto_bicicleta']
            bicicleta.save()
            detalle_usuario.bicicleta = bicicleta
            detalle_usuario.save()

            detalles_etiquetarutausuario = DetalleEtiquetaRutaUsuario.objects.filter(user=user)
            for detalle_etiquetarutausuario in detalles_etiquetarutausuario:
                detalle_etiquetarutausuario.delete()

            if data.get('rutas_interes'):
                for token_tipo_ruta in data['rutas_interes']:
                    etiqueta_ruta = get_or_none(EtiquetaRuta, token=token_tipo_ruta)
                    if etiqueta_ruta is not None:
                        detalle_etiqueta_ruta = DetalleEtiquetaRutaUsuario()
                        detalle_etiqueta_ruta.user = token.user
                        detalle_etiqueta_ruta.etiqueta = etiqueta_ruta
                        detalle_etiqueta_ruta.save()
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Se ha editado un usuario con éxito.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_detalle_usuario', methods=['post'])
    def get_detalle_usuario(self, request):
        try:
            data = request.data
            from django.contrib.auth.models import User
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            id_user = get_or_none(DetalleUsuario, token=data['token_usuario'])
            datos = DetalleUsuario.get_all_informacion(id_user.usuario_id)
            detalle = get_or_none(DetalleUsuario, usuario=token.user)
            if detalle.admin == 0:
                return jsonx({'status': 'error', 'message': 'Debe ser administrador para recibir la data.'})

            for data in datos:
                data['etiquetas'] = DetalleEtiquetaRutaUsuario.get_etiqueta_usuario(id=token.user.id)
                data['rutas'] = InscripcionRuta.get_ruta_inscripcion(id=token.user.id)
                for ruta in data['rutas']:
                    detallearchivo = DetalleArchivoRuta.objects.filter(ruta_id=ruta['id']).first()
                    archivo = Archivo.objects.get(id=detallearchivo.archivo_id)
                    ruta["link"] = archivo.link
                    ruta.pop("id")
            return jsonx({'status': 'success', 'message': 'Información del usuario completa.', 'data': datos})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_usuarios', methods=['get'])
    def get_usuarios(self, request):
        try:
            from django.contrib.auth.models import User
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            #detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            #if detalle_usuario.admin == 0:
            #    return jsonx({'status': 'error', 'message': 'Solo puede acceder a los usuarios un administrador.'})
            datos = DetalleUsuario.get_all_users()
            return jsonx({'status': 'success', 'message': 'Información del usuario completa.', 'data': datos})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='setear_admin', methods=['post'])
    def setear_admin(self, request):
        try:
            data = request.data
            from django.contrib.auth.models import User
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            detalle_usuario = DetalleUsuario.objects.get(usuario=token.user)
            if detalle_usuario.admin == 0:
                return jsonx({'status': 'error', 'message': 'No tiene permiso para realizar esta acción.'})
            usuario = DetalleUsuario.objects.get(token=data['token_usuario'])
            usuario.admin = data['admin']
            usuario.save()
            return jsonx({'status': 'success', 'message': 'Se ha modificado con éxito el usuario.'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})



class DetalleUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleUsuarioSerializer
    queryset = DetalleUsuario.objects.all()
    # lookup_field = 'token_publico'


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        usuario = get_or_none(User,email= request.data.get("user").get("email"))
        if usuario:
            if not usuario.is_active:
                return HttpResponse(status=400, content=json.dumps({"non_field_errors": ["La cuenta no ha sido activada."]}), content_type="application/json")

        # serializer = self.serializer_class(data=request.data['email'], context={'request': request})
        # try:
        #     serializer.is_valid(raise_exception=True)
        # except:
        #     return HttpResponse(status=400, content=json.dumps({"non_field_errors":["No puede iniciar sesión con las credenciales proporcionadas."]}), content_type="application/json")
        detalle_usuario = get_or_none(DetalleUsuario, usuario=usuario)
        # user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=usuario)
        response = {
            'token': token.key,
            # 'token_publico': user.detalleusuario.token_publico, #para no hacer visible el ID se usa token de DetalleUsuario
            # 'id': str(user.id),
            'username': usuario.username,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'email': usuario.email,
            # 'plan': Plan.obtener_plan(request.data['plan'] if request.data.get('plan') != None else None),
            'is_staff': usuario.is_staff,
            'is_superuser': usuario.is_superuser,
            'admin': detalle_usuario.admin,
            'foto': detalle_usuario.foto,
            'genero': detalle_usuario.genero,
            'peso': detalle_usuario.peso,
            'edad': detalle_usuario.edad,
            'nivel': detalle_usuario.nivel,
            'token_notificacion': detalle_usuario.token_notificacion,
            # 'avatar': settings.URL_DJANGO_SERVER + reverse(servir_imagen_perfil, args=[user.detalleusuario.token_publico]),
            # 'socialMedia': False
        }

        # data = request.data.get('user')
        # if data.get("token_publico"):
        #     invitacion = Invitacion.objects.get(token_publico=data.get("token_publico"))
        #     data_invitacion = {
        #         'invitacion': invitacion,
        #         'usuario': user
        #     }
        #     invitacion.aceptarInvitacion(data=data_invitacion)

        return Response(response)


class Logout(APIView):
    def post(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UsuarioRecuperarCredencialesViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioRecuperarClaveSerializer
    queryset = RegistroCambiarClave.objects.filter()

    @action(detail=False, url_path='enviar_email_recuperacion_clave', methods=['post'], permission_classes=[AllowAny])
    def enviar_email_recuperacion(self, request):
        import uuid

        transaction.set_autocommit(False)
        try:
            email = request.data.get('email')  # El unico campo que es unique
            usuario = get_or_none(User, email=email)
            if usuario:
                registro = RegistroCambiarClave(usuario=usuario, token=str(uuid.uuid4()))
                registro.save()
                registro.enviar()
                transaction.commit()
                respuesta = {'status': 'success', 'mensaje': 'Correo de recuperación enviado. Revise su correo electrónico para reiniciar su contraseña.'}
            else:
                transaction.rollback()
                respuesta = {'status': 'error', 'mensaje': 'No se puede realizar la acción.'}

        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'mensaje': str(msg)})
        except Exception as err:
            transaction.rollback()
            return jsonx({'status': 'error', 'mensaje': str(err)})

        return Response(respuesta)


    @action(detail=False, url_path='actualizar_clave', methods=['post'],permission_classes=[AllowAny])
    def actualizar_clave(self, request):
        transaction.set_autocommit(False)

        try:
            token                       = request.data.get('token')
            nueva_clave                 = request.data.get('nueva_clave')
            nueva_clave_confirmacion    = request.data.get('nueva_clave_confirmacion')

            if not token or not nueva_clave or not nueva_clave_confirmacion:
                return Response({'status': 'error', 'mensaje': 'Parámetros insuficientes.'})

            registro = RegistroCambiarClave.objects.get(token=token)
            if nueva_clave == nueva_clave_confirmacion:
                registro.usuario.set_password(nueva_clave)
                registro.usuario.save()
                registro.delete()
                transaction.commit()
                respuesta = {'status': 'success', 'mensaje': 'Clave cambiada con éxito. Por favor inicie sesión.'}
            else:
                transaction.rollback()
                respuesta = {'status': 'error', 'mensaje': 'La confirmación y la nueva clave deben ser iguales.'}


        except ObjectDoesNotExist as e:
            respuesta = {'status': 'error', 'mensaje': 'El token de cambio de clave es incorrecto o está caducado.'}
        except ApplicationError as msg:
            transaction.rollback()
            respuesta = jsonx({'status': 'error', 'mensaje': str(msg)})
        except Exception as err:
            transaction.rollback()
            respuesta = jsonx({'status': 'error', 'mensaje': str(err)})

        return Response(respuesta)

    @action(detail=False, url_path='verificar', methods=['POST'], permission_classes=[AllowAny])
    def verificarToken(self, request):
        token_publico = request.data.get('token')
        respuesta = RegistroCambiarClave.verificarToken(token_publico=token_publico)
        return jsonx({'status': 'success', 'mensaje': 'ok', 'data': respuesta})
