# coding=utf-8
#django
import os
import posixpath
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djangologout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views.static import serve
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from ecuaciclismo.base.models import ImagenTemporal
from ecuaciclismo.base.forms import LoginForm, SolicitarCambioClaveForm, ProcesarCambioClaveOlvidadaForm
from ecuaciclismo.helpers.http import render, redirect
from ecuaciclismo.helpers.decorators import base_login_required
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import handler_403

from ecuaciclismo.settings import URL_PREFIX


USE_XSENDFILE = getattr(settings, 'USE_XSENDFILE', False)


def login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if not user:
                messages.error(request, 'El usuario o password no son válidos.')
            else:
                djangologin(request, user)
                url_redirect = URL_PREFIX + '/reporte/dashboard/'
                return HttpResponseRedirect(url_redirect)
    else:
        form = LoginForm()
    response = render(request, 'login.html', {'form': form, 'next': next})
    return response


def recuperar_clave(request):
    if request.method == 'GET':
        form = SolicitarCambioClaveForm()
    if request.method == 'POST':
        form = SolicitarCambioClaveForm(request.POST)
        if form.is_valid():
            proceso = form.save()
            proceso.enviar()
            messages.info(request, 'Le hemos enviado un email con las instrucciones para recuperar tu cuenta.')
        else:
            messages.error(request, 'Por favor revise el formulario')
    response = render(request, 'recuperar_clave.html', {'form': form})
    return response


def procesar_cambio_clave(request, token = None):
    from ecuaciclismo.base.models import RegistroCambiarClave
    form, registro, consultando, exito = None, None, None, None
    if request.method == "GET":
        if token:
            try:
                registro = RegistroCambiarClave.objects.get(token = token)
                consultando = True
            except RegistroCambiarClave.DoesNotExist:
                return HttpResponseRedirect(reverse(login))
                # messages.info(request, 'El token de cambio de clave es incorrecto o está caducado')

        if registro:
            form = ProcesarCambioClaveOlvidadaForm(usuario = registro.usuario)
    if request.method == "POST":
        try:
            registro = RegistroCambiarClave.objects.get(token = request.POST.get('token'))
        except RegistroCambiarClave.DoesNotExist:
            messages.info(request, 'El token de cambio de clave es incorrecto o está caducado')

        form = ProcesarCambioClaveOlvidadaForm(request.POST, usuario = registro.usuario)
        if form.is_valid():
            form.save()
            registro.delete()
            response = HttpResponseRedirect(reverse(procesar_cambio_clave, args = []))
            messages.success(request, 'Clave cambiada con éxito. Por favor inicie sesión.')
            return response
        else:
            response = HttpResponseRedirect(reverse(procesar_cambio_clave, args = [request.POST.get('token')]))
            messages.error(request, 'La confirmación y la nueva clave deben ser iguales')
            return response
    response = render(request, 'procesar_cambio_clave.html', {'form': form, 'registro': registro, 'consultando': consultando})
    return response


def logout(request):
    djangologout(request)
    # form = LoginForm()
    url_redirect = URL_PREFIX + '/accounts/login/'
    return HttpResponseRedirect(url_redirect)
    # return render(request, 'login.html', {'form': form})


@base_login_required
def index(request):
    """ Vista de la pantalla principal de la aplicación """
    if not request.user or type(request.user) is AnonymousUser:
        return HttpResponseRedirect(URL_PREFIX+'/accounts/login/')
    else:
        return HttpResponseRedirect(URL_PREFIX+'/reporte/dashboard/')


@base_login_required
def mail_recuperar_clave(request):
    """ Vista para probar email """
    response = render(request, 'mail/mail_recuperar_clave.html', {})
    return response


def xsendfileserve_sin_login(request, path, document_root=settings.MEDIA_ROOT,type='inline'):#attachment
    """
	Serve static files using X-Sendfile below a given point
	in the directory structure.

	This is a thin wrapper around Django's built-in django.views.static,
	which optionally uses USE_XSENDFILE to tell webservers to send the
	file to the client. This can, for example, be used to enable Django's
	authentication for static files.

	To use, put a URL pattern such as::

		(r'^(?P<path>.*)$', login_required(xsendfileserve),
							{'document_root' : '/path/to/my/files/'})

	in your URLconf. You must provide the ``document_root`` param. You may
	also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
	of the directory.  This index view will use the template hardcoded below,
	but if you'd like to override it, you can create a template called
	``static/directory_index.html``.
	"""

    if USE_XSENDFILE:
        # This code comes straight from the static file serve
        # code in Django 1.2.

        # Clean up given path to only allow serving files below document_root.
        path = posixpath.normpath(urllib.unquote(path))
        path = path.lstrip('/')
        newpath = ''
        for part in path.split('/'):
            if not part:
                # Strip empty path components.
                continue
            drive, part = os.path.splitdrive(part)
            head, part = os.path.split(part)
            if part in (os.curdir, os.pardir):
                # Strip '.' and '..' in path.
                continue
            newpath = os.path.join(newpath, part).replace('\\', '/')
        if newpath and path != newpath:
            return HttpResponseRedirect(newpath)
        fullpath = os.path.join(document_root, newpath)
        # This is where the magic takes place.
        response = HttpResponse()
        response['X-Sendfile'] = fullpath
        # Unset the Content-Type as to allow for the webserver
        # to determine it.
        response['Content-Type'] = ''
        return response
    path = path.replace("\\", "/")
    response = serve(request, path, document_root)
    response['Content-Disposition'] = type+'; filename=%s' % smart_str(path.split('/')[-1])
    return response

#activate
def activate_account(request, uidb64, token):
    try:
        plan = request.GET.get('plan')
    except Exception as e:
        # print(e)
        plan = 1

    URL = settings.URLC
    HTT = settings.HTTP

    url = HTT + URL + "/web_app/login/?plan="+str(plan)

    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        user.is_active = True
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        from ecuaciclismo.apps.backend.contrato.models import Plan
        from ecuaciclismo.apps.backend.usuario.views import servir_imagen_perfil
        response = {
            'token': token.key,
            'token_publico': user.detalleusuario.token_publico, # para no hacer visible el ID se usa token de DetalleUsuario
            # 'id': str(user.id),
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'plan': Plan.obtener_plan(request.data['plan'] if request.data.get('plan')!= None else None),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'avatar': settings.URL_DJANGO_SERVER + reverse(servir_imagen_perfil, args=[user.detalleusuario.token_publico]),
            'socialMedia': False
        }
        return Response(response)
        # return redirect(url, {'status': 'success', 'mensaje': 'exito', 'user':user})

    else:
        return jsonx({'status': 'error', 'mensaje':'Activation link is invalid!'})

def xsendfileserve_static_sin_login(request, path, document_root=settings.CURRENT_DIR,type='inline'):#attachment
    """
	Serve static files using X-Sendfile below a given point
	in the directory structure.

	This is a thin wrapper around Django's built-in django.views.static,
	which optionally uses USE_XSENDFILE to tell webservers to send the
	file to the client. This can, for example, be used to enable Django's
	authentication for static files.

	To use, put a URL pattern such as::

		(r'^(?P<path>.*)$', login_required(xsendfileserve),
							{'document_root' : '/path/to/my/files/'})

	in your URLconf. You must provide the ``document_root`` param. You may
	also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
	of the directory.  This index view will use the template hardcoded below,
	but if you'd like to override it, you can create a template called
	``static/directory_index.html``.
	"""
    if USE_XSENDFILE:
        # This code comes straight from the static file serve
        # code in Django 1.2.

        # Clean up given path to only allow serving files below document_root.
        path = posixpath.normpath(urllib.unquote(path))
        path = path.lstrip('/')
        newpath = ''
        for part in path.split('/'):
            if not part:
                # Strip empty path components.
                continue
            drive, part = os.path.splitdrive(part)
            head, part = os.path.split(part)
            if part in (os.curdir, os.pardir):
                # Strip '.' and '..' in path.
                continue
            newpath = os.path.join(newpath, part).replace('\\', '/')
        if newpath and path != newpath:
            return HttpResponseRedirect(newpath)
        fullpath = os.path.join(document_root, newpath)
        # This is where the magic takes place.
        response = HttpResponse()
        response['X-Sendfile'] = fullpath
        # Unset the Content-Type as to allow for the webserver
        # to determine it.
        response['Content-Type'] = ''
        return response
    response = serve(request, path, document_root)
    response['Content-Disposition'] = type+'; filename=%s' % smart_str(path.split('/')[-1])
    return response


def encryptedfileserve_sin_login(request, path_archivo_pdf, documento, type ='inline'):
    from ecuaciclismo.helpers.classes import EncriptacionAsimetrica

    #ENCRIPTACION
    data = EncriptacionAsimetrica.desencriptar(path_archivo_pdf, documento)
    #/DESENCRIPTACION

    response = HttpResponse(data, content_type='application/pdf')
    response['Content-Disposition'] = type+'; filename=%s' % str(documento.file)

    return response
