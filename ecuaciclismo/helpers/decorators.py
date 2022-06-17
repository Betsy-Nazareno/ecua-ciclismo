# coding=utf-8

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.http import urlquote

# comextweb
# from ecuaciclismo.apps.backend.configuracion.models import ConfiguracionCuenta
from ecuaciclismo.apps.backend.empresa.models import Empresa, EmpresaUsuario
# from comextweb.base.models import NotificacionUsuario
from ecuaciclismo.helpers.http import get_subdomain
from ecuaciclismo.helpers.jsonx import jsonx
from ecuaciclismo.helpers.tools_utilities import get_or_none
from ecuaciclismo.settings import URL_PREFIX
from functools import wraps

def custom_decorator(func):
    # ADD THIS LINE TO YOUR CUSTOM DECORATOR
    @wraps(func)
    def func_wrapper(viewset,*args, **kwargs):
        request = viewset.request
        usuario = request.user
        subdominio = get_subdomain(request=request)
        if subdominio:
            empresa = get_or_none(Empresa, subdominio=subdominio)
            if not empresa:
                return HttpResponse(status=404)
            empresa_usuario = get_or_none(EmpresaUsuario, empresa=empresa, usuario=usuario)
            if not empresa_usuario and not usuario.is_superuser:
                return HttpResponse(status=403)
            request.empresa=empresa
        else:
            request.empresa = None
        return func(viewset, *args, **kwargs)
    return func_wrapper

def administrador_required(func):
    @wraps(func)
    def func_wrapper(viewset,*args, **kwargs):
        request = viewset.request
        if not request.user.is_superuser:
            return HttpResponse(status=403)
        return func(request, *args, **kwargs)

    return func_wrapper


def custom_decorator_request(func):
    # ADD THIS LINE TO YOUR CUSTOM DECORATOR
    @wraps(func)
    def func_wrapper(request,*args, **kwargs):
        request=request
        subdominio=get_subdomain(request=request)
        empresa=Empresa.objects.get(subdominio=subdominio)
        request.empresa=empresa

        return func(request,*args, **kwargs)
    return func_wrapper


def base_login_required(function):
    def wrapper(request, *args, **kwargs):

        # if not request.user or not request.user.is_authenticated:
        #     return HttpResponseRedirect(URL_PREFIX+'/accounts/login')
        #
        # empresa = Empresa.objects.filter().first()
        # usuario = request.user
         #
        # # if usuario.is_authenticated:
        # if not usuario.is_superuser:
        #     empresa_usuario = get_or_none(EmpresaUsuario,empresa=empresa,usuario=usuario)
        # else:
        #     empresa_usuario = EmpresaUsuario(empresa=empresa,usuario=usuario)
        # # else:
        # #     empresa_usuario = None
        #
        # if not usuario or not usuario.is_authenticated or not empresa_usuario:
        #     path = str(urlquote(request.get_full_path())).replace(settings.URL_PREFIX,'')
        #     tup = settings.LOGIN_URL, REDIRECT_FIELD_NAME, path
        #     redirect_url = '%s?%s=%s' % tup
        #     return HttpResponseRedirect(redirect_url)
        #
        # request.empresa_usuario = empresa_usuario
        # request.empresa = empresa
        request.empresa= 'prueba'
        return function(request, *args, **kwargs)
    return wrapper

def revisar_tramite_decorator(func):
    # ADD THIS LINE TO YOUR CUSTOM DECORATOR
    @wraps(func)
    def func_wrapper(viewset,*args, **kwargs):
        from ecuaciclismo.apps.backend.tramite.models import Tramite

        request = viewset.request

        # if request.query_params.__contains__('tramite_id'):
        #     tramite = get_object_or_404(Tramite, pk=request.query_params['tramite_id'])
        if request.query_params.__contains__('tramite_token'):
            tramite = get_object_or_404(Tramite, token=request.query_params['tramite_token'])
        else:
            return HttpResponse(status=404)

        if not request.user.is_superuser and not tramite.tiene_permiso_editar(request.user, request.empresa):
            return HttpResponse(status=404)

        return func(viewset, *args, **kwargs)
    return func_wrapper
