import json
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from ecuaciclismo.apps.backend.api.usuario.serializers import DetalleUsuarioSerializer, \
    UsuarioRecuperarClaveSerializer
from ecuaciclismo.apps.backend.ruta.models import InscripcionRuta, DetalleArchivoRuta, Archivo, EtiquetaRuta
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario, Bicicleta, DetalleEtiquetaRutaUsuario, ContactoSeguro,GrupoContactoSeguro
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
            detalle_usuario.telefono= data['telefono']
            detalle_usuario.peso = data['peso']
            if detalle_usuario.bicicleta is None:
                bicicleta = Bicicleta()
            else:
                bicicleta = Bicicleta.objects.get(id=detalle_usuario.bicicleta_id)
            bicicleta.marca = data['marca']
            bicicleta.tipo = data['tipoBicicleta']
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
            ##print(id_user.usuario.id)
            #print(id_user.id)
            datos = DetalleUsuario.get_all_informacion(id_user.usuario_id)
            detalle = get_or_none(DetalleUsuario, usuario=token.user)
            #print(token.user.id)
            #print(id_user.usuario.id)
            if token.user.id != id_user.usuario.id:
                if detalle.admin == 0:
                    return jsonx({'status': 'error', 'message': 'Debe ser administrador para recibir la data.'})

            for data in datos:
                data['etiquetas'] = DetalleEtiquetaRutaUsuario.get_etiqueta_usuario(id=id_user.usuario.id)
                data['rutas'] = InscripcionRuta.get_ruta_inscripcion(id=id_user.usuario.id)
                
                if(data.get('rutas')):
                    for ruta in data['rutas']:
                        detallearchivo = DetalleArchivoRuta.objects.filter(ruta_id=ruta['id']).first()
                        if detallearchivo is not None:
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
    @action(detail=False, url_path='agregar_contacto_seguro', methods=['post'])
    def agregar_contacto_seguro(self, request):
        transaction.set_autocommit(False)
        try:
            data = request.data
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            from django.contrib.auth.models import User
            contacto_seguro = ContactoSeguro()
            if int(request.data['isUser'])==1:
                dataUser= DetalleUsuario.get_all_informacion(data['user_id'])
                contacto_seguro_qs = ContactoSeguro.objects.filter(user=data['user_id'])
                contacto_seguro.user= User.objects.get(id=data['user_id'])
                contacto_seguro.nombre=dataUser[0]['first_name']+ ' '+ dataUser[0]['last_name']
                contacto_seguro.celular=dataUser[0]['telefono']
                contacto_seguro.isUser=1

            else:
                contacto_seguro.isUser=0
                contacto_seguro_qs = ContactoSeguro.objects.filter(nombre=data['nombre'],celular=data['celular'], isUser=0)
                contacto_seguro.nombre=data['nombre']
                contacto_seguro.celular=data['celular']
            
            if contacto_seguro_qs.exists():
                tk= contacto_seguro_qs.first().token
                cs=get_or_none(ContactoSeguro, token=tk)
                grupo_contacto_qs=GrupoContactoSeguro.objects.filter(user=token.user_id,contacto_seguro=cs)
                if grupo_contacto_qs.exists():
                    return jsonx({'status': 'error', 'message': 'El contacto seguro ya existe'})

            contacto_seguro.save()
            grupo_contacto_seguro = GrupoContactoSeguro()
            grupo_contacto_seguro.user=User.objects.get(id=token.user_id)
            grupo_contacto_seguro.contacto_seguro=contacto_seguro
            grupo_contacto_seguro.save()
            transaction.commit()
            return jsonx({'status': 'success', 'message': 'Se ha agregado un nuevo contacto seguro'})
        except ApplicationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(msg)})
        except ValidationError as msg:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            transaction.rollback()
            return jsonx({'status': 'error', 'message': str(e)})
    
    @action(detail=False, url_path='delete_contacto_seguro', methods=['delete'], permission_classes=[AllowAny])
    def delete_contacto_seguro(self, request):
        try:
            data = request.data
            contactoPorEliminar= get_or_none(ContactoSeguro, token=data['token_contacto'])
            contactoPorEliminar.delete()
            #grupo_contacto_seguro=GrupoContactoSeguro.objects.get(user=usuario, contacto_seguro=contactoPorEliminar)
            #grupo_contacto_seguro.delete()
            return jsonx({'status': 'success', 'message': 'Se ha eliminado el contacto seguro'})
        except ApplicationError as msg:
            return jsonx({'status': 'error', 'message': str(msg)})
        except (User.DoesNotExist, ContactoSeguro.DoesNotExist, GrupoContactoSeguro.DoesNotExist):
            return jsonx({'status': 'error', 'message': 'El usuario o el contacto seguro no existen o no están asociados.'})
        except ValidationError as msg:
            return jsonx({'status': 'error', 'message': list(msg)})
        except Exception as e:
            return jsonx({'status': 'error', 'message': str(e)})

    @action(detail=False, url_path='get_contactos_seguros', methods=['get'])
    def get_contactos_seguros(self, request):
        try:
            from django.contrib.auth.models import User
            from rest_framework.authtoken.models import Token
            token = Token.objects.get(key=request.headers['Authorization'].split('Token ')[1])
            datos = GrupoContactoSeguro.get_contactos_seguros_usuario(token.user_id)
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


class DetalleUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleUsuarioSerializer
    queryset = DetalleUsuario.objects.all()
    # lookup_field = 'token_publico'


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get("user").get("email")
        password = request.data.get("user").get("password")
        print(password)
        usuario = get_or_none(User, email=email)
        print(usuario)
        if usuario is not None:
            # Se verifica si el usuario está activo
            if not usuario.is_active:
                return HttpResponse(
                    status=400,
                    content=json.dumps({"non_field_errors": ["La cuenta no ha sido activada."]}),
                    content_type="application/json"
                )

            # Se autentica al usuario con las credenciales proporcionadas
            user = None
            if usuario.check_password(password):
                user = usuario
            print(user)
            if user is not None:
                detalle_usuario = get_or_none(DetalleUsuario, usuario=usuario)
                if request.data.get("user").get("token_notificacion"):
                    detalle_usuario.token_notificacion = request.data.get("user").get("token_notificacion")
                    detalle_usuario.save()

                # Se crea o se obtiene el token de autenticación
                token, created = Token.objects.get_or_create(user=usuario)

                response = {
                    'token': token.key,
                    'id_usuario': detalle_usuario.token,
                    'username': usuario.username,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name,
                    'email': usuario.email,
                    'is_staff': usuario.is_staff,
                    'is_superuser': usuario.is_superuser,
                    'is_active': usuario.is_active,
                    'admin': detalle_usuario.admin,
                    'foto': detalle_usuario.foto,
                    'genero': detalle_usuario.genero,
                    'telefono': detalle_usuario.telefono,
                    'peso': detalle_usuario.peso,
                    'edad': detalle_usuario.edad,
                    'nivel': detalle_usuario.nivel,
                    'tipo': detalle_usuario.tipo,
                    'token_notificacion': detalle_usuario.token_notificacion,
                }

                return Response(response)
        
        return HttpResponse(
            status=400,
            content=json.dumps({"non_field_errors": ["No puede iniciar sesión con las credenciales proporcionadas."]}),
            content_type="application/json"
        )

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
            print(email)
            usuario = get_or_none(User, email=email)
            if usuario:
                registro = RegistroCambiarClave(usuario=usuario, token=str(uuid.uuid4()))
                registro.save()
                registro.enviar()
                transaction.commit()
                respuesta = {'status': 'success', 'mensaje': 'Correo de recuperación enviado. Revise su correo electrónico para reiniciar su contraseña.'}
            else:
                transaction.rollback()
                respuesta = {'status': 'error', 'mensaje': 'El Correo No Existe'}

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
                return render(request, 'exito.html')
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
    

    @action(detail=False, url_path='reset_password/(?P<token>[^/.]+)', methods=['get'], permission_classes=[AllowAny])
    def reset_password(self, request, token=None):
        try:
            registro = get_or_none(RegistroCambiarClave, token=token)
            if (registro is None):
                return render(request, 'password-reset.html')
            
            usuario = get_object_or_404(User, id=registro.usuario_id)
            return render(request, 'password-confirm.html', {'token': token})
        except RegistroCambiarClave.DoesNotExist:
            return render(request, 'password_reset_error.html')
        except User.DoesNotExist:
            return render(request, 'password_reset_error.html')