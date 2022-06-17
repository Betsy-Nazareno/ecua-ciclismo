# coding=utf-8
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect as redirect_to_response
from django.shortcuts import render as render_django

def get_subdomain(request):
    """ Obtiene el subdominio con el nombre corto que utiliza la empresa """
    # host = request.META.get('HTTP_REFERER')
    # print("---------------------------- HOST-")
    # print(host)
    # print("*************************get_host*")
    # print(request.get_host())
    # print("///////////////////////////////////////////////////////////////////////////////////")
    #produccion
    # host = request.get_host()
    # if host != settings.LOCAL_DIRECCION:
    #     i = host.find(settings.URL)
    #     subdomain = host.split('.')
    #     if i == 0:
    #         subdomain = ''
    #     elif i > 0:
    #         subdomain = subdomain[0]
    #     return subdomain if subdomain != '' else None
    #
    # #local
    # else:

    host = request.META.get('HTTP_REFERER')
    if host:
        i = host.find(settings.URL)
        http_index = host.find('//')
        subdomain = host[http_index+2:i - 1].split('.')
        if subdomain[0] == 'www':
            subdomain = subdomain[1]
        else:
            subdomain = subdomain[0]
        return subdomain if subdomain != '' else None

    else:
        host = request.get_host()
        if host != settings.LOCAL_DIRECCION:
            i = host.find(settings.URL)
            subdomain = host.split('.')
            if i == 0:
                subdomain = ''
            elif i > 0:
                subdomain = subdomain[0]
            return subdomain if subdomain != '' else None

        else:
            return None

        # http_index = host.find('//')
        # subdomain = host[http_index+2:i - 1].split('.')
        # if subdomain[0] == 'www':
        #     subdomain = subdomain[1]
        # else:
        #     subdomain = subdomain[0]
        # return subdomain if subdomain != '' else None


    # if i > 0:
    #     host = host[0:i - 1]
    #     if host != 'www':
    #         host = host.replace('www.','').replace(settings.HTTP,'')
    #         return host
    # return None

def render(request, template, dict={}):
    dict.update({'settings': settings})
    return render_django(request, template, context=dict)

def redirect(to, dict=None):
    return redirect_to_response(to, dict)