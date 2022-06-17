# coding=utf-8
# import StringIO
# import logging


import calendar
import os
import sys
import unicodedata
import shutil
# import zipfile
# from cStringIO import StringIO
# from datetime import date, timedelta
# from datetime import datetime
# from decimal import Decimal, ROUND_HALF_UP
from email.mime.image import MIMEImage
# from pdf2image import convert_from_path
from os.path import abspath, join
import re
import time
import zipfile
import io
# try:
#     set
# except NameError:
# from sets import set #Set
# import Set
from django.utils.encoding import smart_str
# from pytz import unicode
# import unidecode as unidecode


try:
    set
except NameError:
    from sets import Set as set

#
# # para crear thumbnail
# from PIL import Image
from django.conf import settings
# from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.template import loader  # , RenderContext
# from django.template import Context, loader
# from django.utils.encoding import smart_str
from django.views.static import serve

from ecuaciclismo.helpers.jsonx import jsonx
#
# from comextweb.helpers.num2word.num2word_ES import *
# from ecuaciclismo.helpers.trml2pdf import trml2pdf_new

# def convert(file, outputDir):
#     outputDir = outputDir + str(round(time.time())) + '/'
#     if not os.path.exists(outputDir):
#         os.makedirs(outputDir)
#
#     pages = convert_from_path(file, 500)
#     counter = 1
#     for page in pages:
#         myfile = outputDir +'output' + str(counter) +'.jpg'
#         counter = counter + 1
#         page.save(myfile, "JPEG")
#         print(myfile)

# from comextweb.settings import URL
#
# logger = logging.getLogger('django')
#
#
# # admin.autodiscover()
#
# class DeleteRelatedError(Exception):
#     pass
#
#
class ApplicationError(Exception):
    def __init__(self, msg):
        """ Constructor de la excepción, debe recibir el mensaje en formato unicode """
        #if not isinstance(msg, unicode): raise Exception('El mensaje de aplicación error debe ser unicode')
        # if not str(type(msg)) == "<type 'unicode'>": raise Exception('El mensaje de aplicación error debe ser unicode')
        self.msg = msg

    def __str__(self):
        return self.msg.encode('utf-8')

    def __unicode__(self):
        """ Representación en Unicode de la excepción """
        return self.msg
#
#
# # PAGINADOR
#
# # NEW PAGINATOR
#
# class InvalidPage(Exception):
#     pass
#
#
# class PageNotAnInteger(InvalidPage):
#     pass
#
#
# class EmptyPage(InvalidPage):
#     pass
#
#
# class NewPaginator(object):
#     def __init__(self, object_list, per_page, number, orphans=0, allow_empty_first_page=True):
#         self.number = number
#         self.object_list = object_list
#         self.per_page = per_page
#         self.orphans = orphans
#         self.allow_empty_first_page = allow_empty_first_page
#
#     # self._num_pages = self._count = None
#
#     def validate_number(self, number):
#         "Validates the given 1-based page number."
#         try:
#             number = int(number)
#         except ValueError:
#             raise PageNotAnInteger('That page number is not an integer')
#         if number < 1:
#             raise EmptyPage('That page number is less than 1')
#         return number
#
#     def page(self, number):
#         "Returns a Page object for the given 1-based page number."
#         number = self.validate_number(number)
#         return Page(self.object_list, number, self)
#
#     def _get_page_range(self):
#         """
#         Returns a 1-based range of pages for iterating through within
#         a template for loop.
#         """
#         return range(1, self.num_pages + 1)
#
#     page_range = property(_get_page_range)
#
#
# QuerySetPaginator = NewPaginator  # For backwards-compatibility.
#
#
# # NEW PAGINATOR
#
# class Page(object):
#     def __init__(self, object_list, number, paginator):
#         self.object_list = object_list
#         self.number = number
#         self.paginator = paginator
#
#     def has_next(self):
#         return len(self.paginator.object_list) > (self.paginator.per_page - 1)
#
#     def has_previous(self):
#         return self.number > 1
#
#     def has_other_pages(self):
#         return self.has_previous() or self.has_next()
#
#     def next_page_number(self):
#         return self.number + 1
#
#     def previous_page_number(self):
#         return self.number - 1
#
#
# # PAGINADOR
#
def mediaurl(request, application="shell", folder=None, path=""):
    """ Sirve los recursos que se encuentran en la carpeta media de las aplicaciones"""
    f = abspath(join(settings.CURRENT_DIR, application, folder))
    return serve(
        request,
        path,
        document_root=f,
        show_indexes=True,
    )
#
#
# def mediaurl2(request, application="shell", folder=None, path=""):
#     """ Sirve los recursos que se encuentran en la carpeta media de las aplicaciones"""
#     f = abspath(join(settings.CURRENT_DIR, application, folder))
#     return serve(
#         request,
#         path,
#         document_root=f,
#         show_indexes=True,
#     )
#
#
# def uploadurl(request, path):
#     """ Sirve los documentos que se encuentran en la carpeta upload
#     Cada aplicación que haga uso de esta vista debe verificar los permisos que debe tener
#     el usuario """
#     f = abspath(join(dirname(__file__), "../../..", 'upload')).replace('\\', '/')
#     path = path.replace('\\', '/')
#     response = serve(
#         request,
#         path,
#         document_root=f,
#         show_indexes=True,
#     )
#     response['Content-Disposition'] = 'inline; filename=%s' % path.split('/')[-1].replace('_', '')
#     return response
#
#
def remove_keys_endswidth(dict, criteria):
    """ Remueve las llaves que terminan con criteria """
    for key in list(dict):
        if key[len(criteria) * -1:] == criteria: del dict[key]
    # for k in dict.keys():
    #     if k[len(criteria) * -1:] == criteria: del dict[k]


def filter_dict(dict, prefix):
    """Takes a dictionary and returns only the items whose key starts with
    the prefix followed by a dash."""
    new_dict = {}
    prefix = prefix + "-"
    keys = [a for a in dict.keys() if a.startswith(prefix)]
    for k in keys: new_dict[k] = dict[k]
    return new_dict


def find_prefix(prefix_re, data):
    r = re.compile(prefix_re)
    return set([m[0] for m in [r.findall(key) for key in data.keys()] if m])
#
#
# def prefix_dict(dict, prefix):
#     newdict = {}
#     for k, v in dict.items():
#         newdict[prefix + '-' + k] = v
#     return newdict
#
#
# def prefix_remove_dict(dict, prefix):
#     """ Filtra el diccionario con los llaves que tengan el prefijo prefix.
#     Una vez filtrado devuelve un nuevo diccionario removiendo el prefijo en las llaves """
#     new_dict = {}
#     prefix = prefix + "-"
#     keys = [a for a in dict.keys() if a.startswith(prefix)]
#     for k in keys: new_dict[k[len(prefix):]] = dict[k]
#     return new_dict
#
#
def email_embed_image(email, img_content_id, img_data):
    """
    email is a django.core.mail.EmailMessage object
    """
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    # img.add_header('Content-Type', 'multipart/alternative')
    img.add_header('Content-Disposition', 'inline')
    email.attach(img)

def email_embed_logos(msg):
    email_embed_image(msg, 'email-template-logo-facebook',
                      open('%sbase/templates/email_templates/img/facebook.png' % settings.STATIC_ROOT,
                           'rb').read())
    email_embed_image(msg, 'email-template-logo-twitter',
                      open('%sbase/templates/email_templates/img/twitter.png' % settings.STATIC_ROOT,
                           'rb').read())
    email_embed_image(msg, 'email-template-logo-instagram',
                      open('%sbase/templates/email_templates/img/instagram.png' % settings.STATIC_ROOT,
                           'rb').read())
    email_embed_image(msg, 'email-template-logo-tiktok',
                      open('%sbase/templates/email_templates/img/tiktok.png' % settings.STATIC_ROOT,
                           'rb').read())
    email_embed_image(msg, 'email-template-logo-linkedin',
                      open('%sbase/templates/email_templates/img/linkdin.png' % settings.STATIC_ROOT,
                           'rb').read())
    email_embed_image(msg, 'email-template-logo-youtube',
                      open('%sbase/templates/email_templates/img/youtube.png' % settings.STATIC_ROOT,
                           'rb').read())
#
#
# def email_embed_image_pro(email, img_content_id, img_data, related_message):
#     """
#     email is a django.core.mail.EmailMessage object
#     """
#     img = MIMEImage(img_data)
#     img.add_header('Content-ID', '<%s>' % img_content_id)
#     # img.add_header('Content-Type', 'multipart/alternative')
#     img.add_header('Content-Disposition', 'inline')
#     related_message.attach(img)
#     email.attach(related_message)
#
#
# def nice(niceness):
#     import os
#     if os.name == 'posix':
#         os.nice(niceness)
#
#
# def render_pdf(request, nombre_archivo, titulo, template, params, generar_numpaginas=True, mostrar_logo=True, tipo='inline', solo_renderizar_archivo=False):
#     """ Función que devuelve un pdf al response según los parámetros específicados """
#     """" tipo = inline si se desea abrir, tipo = attachment si se desea descargar """
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = tipo+';filename=%s.pdf' % nombre_archivo
#     response['Content-Transfer-Encoding'] = "binary"
#     response['Expires'] = "0"
#     t = loader.get_template(template)
#     params['settings'] = settings
#     params['request'] = request
#     params['nombre_archivo'] = nombre_archivo
#     params['titulo'] = titulo
#     params['mostrar_logo'] = mostrar_logo
#     params['render_static_root'] = settings.CURRENT_ROOT
#     if generar_numpaginas:
#         params['numpaginas'] = trml2pdf_new.get_total_pages(t.render(params).encode('utf-8'))
#     if solo_renderizar_archivo:
#         return trml2pdf_new.parseString(t.render(params).encode('utf-8'), http_response=response)
#     else:
#         trml2pdf_new.parseString(t.render(params).encode('utf-8'), http_response=response)
#         return response
#     # response = trml2pdf_new.parseString(t.render(params).encode('utf-8'), http_response=response)
#     # return response

#
# def compress_listnamefiles_to_zipfile(list_name_files=None,name_zip_folder='files'):
#
#     # Open StringIO to grab in-memory ZIP contents
#     s = StringIO.StringIO()
#
#     # The zip compressor
#     zf = zipfile.ZipFile(s, "w")
#
#     for fpath in list_name_files:
#         # Calculate path for file in zip
#         fdir, fname = os.path.split(fpath)
#         zip_path = os.path.join(name_zip_folder, fname)
#
#         # Add file, at correct path
#         zf.write(fpath, zip_path, zipfile.ZIP_DEFLATED)
#
#     # Must close zip for all contents to be written
#     zf.close()
#
#     return s
#
#
# def compress_path_to_zipfile(root_path=None,name_zip_folder='files'):
#
#     # Open StringIO to grab in-memory ZIP contents
#     s = io.BytesIO()
#
#     # The zip compressor
#     zf = zipfile.ZipFile(s, "w")
#
#     # print root_path
#
#     for root, subdirs, files in os.walk(root_path):
#         # print('--\nroot = ' + root)
#         for subdir in subdirs:
#             # print('\t- subdirectory ' + subdir)
#             pass
#
#         for filename in files:
#             file_path = os.path.join(root, filename)
#
#             # print('\t- file %s (full path: %s)' % (filename, file_path))
#             # print subdir
#             # print file_path
#             fdir, fname = os.path.split(file_path)
#             zip_path = os.path.join(name_zip_folder, fname)
#             zf.write(file_path, zip_path,zipfile.ZIP_DEFLATED)#zipfile.ZIP_DEFLATED#zipfile.ZIP_STORED
#
#     # Must close zip for all contents to be written
#     zf.close()
#     return s.getvalue()
def compress_path_to_zipfile(root_path=None,name_zip_folder='files', directorio_firmados='documentos_firmados'):
    DIRECTORIO_ORIGINAL = "documentos"
    # DIRECTORIO_FIRMADOS = "documentos_firmados"
    DIRECTORIO_FIRMADOS = directorio_firmados
    # Open StringIO to grab in-memory ZIP contents
    s = io.BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    # print root_path
    directorios = [DIRECTORIO_ORIGINAL, DIRECTORIO_FIRMADOS]
    for directorio in directorios:
        path_actual= os.path.join(root_path,directorio)
        for root, subdirs, files in os.walk(path_actual):
            # print('--\nroot = ' + root)
            for subdir in subdirs:
                # print('\t- subdirectory ' + subdir)
                pass

            for filename in files:
                file_path = os.path.join(root, filename)

                # print('\t- file %s (full path: %s)' % (filename, file_path))
                # print subdir
                # print file_path
                fdir, fname = os.path.split(file_path)
                # print("+++++++++++++++")
                # print('fdir %s ---- fname %s' % (fdir, fname))
                zip_path = os.path.join(name_zip_folder, directorio,fname)
                zf.write(file_path, zip_path,zipfile.ZIP_DEFLATED)#zipfile.ZIP_DEFLATED#zipfile.ZIP_STORED

    # Must close zip for all contents to be written
    zf.close()
    return s.getvalue()


def compress_encrypted_path_to_zipfile(root_path=None,name_zip_folder='files', directorio_firmados='documentos_firmados'):
    from ecuaciclismo.helpers.classes import EncriptacionAsimetrica
    from ecuaciclismo.apps.backend.tramite.models import Documento, Tramite


    DIRECTORIO_ORIGINAL = "documentos"
    # DIRECTORIO_FIRMADOS = "documentos_firmados"
    DIRECTORIO_FIRMADOS = directorio_firmados
    # Open StringIO to grab in-memory ZIP contents
    s = io.BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    # print root_path
    directorios = [DIRECTORIO_ORIGINAL, DIRECTORIO_FIRMADOS]
    for directorio in directorios:
        path_actual= os.path.join(root_path,directorio)
        for root, subdirs, files in os.walk(path_actual):
            # print('--\nroot = ' + root)
            for subdir in subdirs:
                # print('\t- subdirectory ' + subdir)
                pass

            for filename in files:
                file_path = os.path.join(root, filename)

                # print("************************************")
                # print('\t- file %s (full path: %s)' % (filename, file_path))
                # print("************************************")
                # print subdir
                # print file_path
                # fdir, fname = os.path.split(file_path)
                # zip_path = os.path.join(name_zip_folder, directorio,fname)
                # zf.write(file_path, zip_path,zipfile.ZIP_DEFLATED)#zipfile.ZIP_DEFLATED#zipfile.ZIP_STORED

                if filename.endswith(EncriptacionAsimetrica.EXTENSION_FILE_PDF_CIFRADO):
                    token_documento = filename.split("_")[-2]
                    documento = Documento.objects.get(token=token_documento)

                    prefijo = ''
                    if directorio == Tramite.DIRECTORIO_FIRMADOS_ELECTRONICA or directorio == Tramite.DIRECTORIO_FIRMADOS_DIGITAL:
                        prefijo = 'signed_'

                    # ENCRIPTACION
                    # print("+++++++++++++++++++++++++++++++++++++")
                    # print(os.path.join(root, prefijo + str(documento.file)))
                    data = EncriptacionAsimetrica.desencriptar(os.path.join(root, prefijo + str(documento.file)), documento)
                    # /ENCRIPTACION

                    zip_path = os.path.join(name_zip_folder, directorio, prefijo + str(documento.file))

                    zf.writestr(zip_path, data, zipfile.ZIP_DEFLATED)


    # Must close zip for all contents to be written
    zf.close()
    return s.getvalue()


#
#
# def moneda_a_letras(valor):
#     entero, fraccion = 0, u'con 00/100 dólares'
#     if type(valor) == float:
#         valor = Decimal(str(valor))
#     valor = valor.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
#     valor = str(valor)
#     pos_punto = valor.find('.')
#     if pos_punto <> -1:
#         entero = long(valor[0:pos_punto])
#         fraccion = u'con %s/100 dólares' % valor[pos_punto + 1:]
#     else:
#         entero = long(valor[0:pos_punto])
#     return (u'%s %s' % (unicode(to_card(entero), 'utf-8'), fraccion)).capitalize()
#
#
# def fecha_a_letras(fecha, ciudad):
#     mes = ''
#     if str(fecha.month) == '1' or str(fecha.month) == '01':
#         mes = 'enero'
#     if str(fecha.month) == '2' or str(fecha.month) == '02':
#         mes = 'febrero'
#     if str(fecha.month) == '3' or str(fecha.month) == '03':
#         mes = 'marzo'
#     if str(fecha.month) == '4' or str(fecha.month) == '04':
#         mes = 'abril'
#     if str(fecha.month) == '5' or str(fecha.month) == '05':
#         mes = 'mayo'
#     if str(fecha.month) == '6' or str(fecha.month) == '06':
#         mes = 'junio'
#     if str(fecha.month) == '7' or str(fecha.month) == '07':
#         mes = 'julio'
#     if str(fecha.month) == '8' or str(fecha.month) == '08':
#         mes = 'agosto'
#     if str(fecha.month) == '9' or str(fecha.month) == '09':
#         mes = 'septiembre'
#     if str(fecha.month) == '10':
#         mes = 'octubre'
#     if str(fecha.month) == '11':
#         mes = 'noviembre'
#     if str(fecha.month) == '12':
#         mes = 'diciembre'
#
#     if ciudad:
#         st = ciudad + ', ' + str(fecha.day) + ' de ' + mes + ' del ' + str(fecha.year)
#     else:
#         st = str(fecha.day) + ' de ' + mes + ' del ' + str(fecha.year)
#     return st
#
#
# def moneda_a_letrasC(valor):
#     entero, fraccion = 0, u' 00/100'
#     if type(valor) == float:
#         valor = Decimal(str(valor))
#     valor = valor.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
#     valor = str(valor)
#     pos_punto = valor.find('.')
#     if pos_punto <> -1:
#         entero = long(valor[0:pos_punto])
#         fraccion = u' %s/100' % valor[pos_punto + 1:]
#     else:
#         entero = long(valor[0:pos_punto])
#     return (u'%s %s' % (unicode(to_card(entero), 'utf-8'), fraccion)).capitalize()
#
#
# def get_week_days(year, week):
#     d = date(year, 1, 1)
#     if (d.weekday() > 3):
#         d = d + timedelta(7 - d.weekday())
#     else:
#         d = d - timedelta(d.weekday())
#     dlt = timedelta(days=(week - 1) * 7)
#     return d + dlt, d + dlt + timedelta(days=6)
#
#
# def get_day_name(day):
#     if day == 0:
#         return 'Lunes'
#     elif day == 1:
#         return 'Martes'
#     elif day == 2:
#         return 'Miercoles'
#     elif day == 3:
#         return 'Jueves'
#     elif day == 4:
#         return 'Viernes'
#     elif day == 5:
#         return 'Sabado'
#     else:
#         return 'Domingo'
#
#
# def get_month_name(month):
#     mes = ''
#     if str(month) == '1' or str(month) == '01':
#         mes = 'Enero'
#     if str(month) == '2' or str(month) == '02':
#         mes = 'Febrero'
#     if str(month) == '3' or str(month) == '03':
#         mes = 'Marzo'
#     if str(month) == '4' or str(month) == '04':
#         mes = 'Abril'
#     if str(month) == '5' or str(month) == '05':
#         mes = 'Mayo'
#     if str(month) == '6' or str(month) == '06':
#         mes = 'Junio'
#     if str(month) == '7' or str(month) == '07':
#         mes = 'Julio'
#     if str(month) == '8' or str(month) == '08':
#         mes = 'Agosto'
#     if str(month) == '9' or str(month) == '09':
#         mes = 'Septiembre'
#     if str(month) == '10':
#         mes = 'Octubre'
#     if str(month) == '11':
#         mes = 'Noviembre'
#     if str(month) == '12':
#         mes = 'Diciembre'
#     return mes
#
#
# def get_num_format_str(num):
#     if num == 2:
#         return '#,##0.00'
#     elif num == 3:
#         return '#,##0.000'
#     elif num == 4:
#         return '#,##0.0000'
#     else:  # num = 5
#         return '#,##0.00000'
#
#
def procesar_autocompletar(datos, descripcion=True):
    result = []
    for dato in datos:
        label = dato[2] if descripcion else dato[1]
        result.append({'id': dato[0],
                       'label': label,
                       'value': dato[1]})
    return jsonx(result)

def procesar_autocompletar_persona(datos):
    result = []
    for dato in datos:
        # print(dato)
        result.append({'token': dato[0],
                       'label': dato[1],
                       'value': dato[1]})
    return jsonx(result)

def setear_representaciones_finders_fields(formulario,data):
    if data:
        data_keys = data.keys()
        for field in formulario:
            if field.name+'_representacionff' in data_keys:
                formulario.fields[field.name].widget.attrs['representacionff'] = data[field.name+'_representacionff']
                formulario.fields[field.name].widget.attrs['objdataff'] = str(data)


# def procesar_autocompletar_handsome(datos, descripcion=True):
#     from comextweb.helpers.jsonx import json
#     result = []
#     dict = {}
#     # {
#     # "data": ["Acura","Audi","BMW","Buick","Cadillac","Chevrolet","Chrysler","Citroen","Dodge","Eagle","Ferrari","Ford","General Motors","GMC","Honda","Hummer","Hyundai","Infiniti","Isuzu","Jaguar","Jeep","Kia","Lamborghini","Land Rover","Lexus","Lincoln","Lotus","Mazda","Mercedes-Benz","Mercury","Mitsubishi","Nissan","Oldsmobile","Peugeot","Pontiac","Porsche","Regal","Renault","Saab","Saturn","Seat","Skoda","Subaru","Suzuki","Toyota","Volkswagen","Volvo"]
#     # }
#     # dict['data'] = ['Carrito','Yujuuuuu','Acura','Audi','BMW','Buick','Cadillac','Chevrolet','Chrysler','Citroen','Dodge','Eagle','Ferrari','Ford','General Motors','GMC','Honda','Hummer','Hyundai','Infiniti','Isuzu','Jaguar','Jeep','Kia','Lamborghini','Land Rover','Lexus','Lincoln','Lotus','Mazda','Mercedes-Benz','Mercury','Mitsubishi','Nissan','Oldsmobile','Peugeot','Pontiac','Porsche','Regal','Renault','Saab','Saturn','Seat','Skoda','Subaru','Suzuki','Toyota','Volkswagen','Volvo']
#     # aaa = {'data': ['Acura','Audi','BMW','Buick','Cadillac','Chevrolet','Chrysler','Citroen','Dodge','Eagle','Ferrari','Ford','General Motors','GMC','Honda','Hummer','Hyundai','Infiniti','Isuzu','Jaguar','Jeep','Kia','Lamborghini','Land Rover','Lexus','Lincoln','Lotus','Mazda','Mercedes-Benz','Mercury','Mitsubishi','Nissan','Oldsmobile','Peugeot','Pontiac','Porsche','Regal','Renault','Saab','Saturn','Seat','Skoda','Subaru','Suzuki','Toyota','Volkswagen','Volvo']}"
#     # return json(dict)
#
#     for dato in datos:
#         # label = dato[2] if descripcion else dato[1]
#         result.append(dato[2])
#     dict['data'] = result
#     return json(dict)
#
#
# class MensajeHtml(object):
#     @classmethod
#     def javascript(cls, texto):
#         return """<script type="text/javascript">""" + texto + """</script>"""
#
#     @classmethod
#     def exitoso(cls, texto):
#         return """<div class="row mensajeInformacion">
#                 <div class="col-md-12">
#                     <div class="alert alert-success">
#                         <a aria-hidden="true" href="#" data-dismiss="alert" class="close">×</a>
#                         <span class="glyphicon glyphicon-ok-sign"></span>
#                         <strong>Información:</strong>""" + texto + """
#                     </div>
#                     <br>
#                 </div>
#             </div>"""
#
#     @classmethod
#     def error(cls, texto):
#         return """<div class="row">
#                 <div class="col-md-12">
#                     <div class="alert alert-danger">
#                         <a aria-hidden="true" href="#" data-dismiss="alert" class="close">×</a>
#                         <span class="glyphicon glyphicon-exclamation-sign"></span>
#                         <strong>Error:</strong>""" + texto + """
#                     </div>
#                     <br>
#                 </div>
#             </div>"""
#
#
# def build_url(prefix, suffix, is_secure):
#     url_builder = 'http'
#     if is_secure:
#         url_builder += 's'
#     return url_builder + '://%s.%s%s' % (prefix, URL, suffix)
#
#
# def build_url_public(suffix, is_secure):
#     url_builder = 'http'
#     if is_secure:
#         url_builder += 's'
#     return url_builder + '://%s%s' % (URL, suffix)
#
#
# def transform_price(base):
#     if not re.match("^\d+((,|.)?\d\d?)?$", base):
#         return 0
#     if re.search("(,|\.)", base):
#         numbers = re.split("(,|\.)", base)
#         if len(numbers[2]) == 1:
#             numbers[2] += "0"
#         return numbers[0] + numbers[2]
#     return base + "00"
#
#
# def get_hexdigest(algorithm, salt, raw_password):
#     import hashlib
#     from django.utils.encoding import smart_str
#     """
#     Returns a string of the hexdigest of the given plaintext password and salt
#     using the given algorithm ('md5', 'sha1' or 'crypt').
#     """
#     raw_password, salt = smart_str(raw_password), smart_str(salt)
#     if algorithm == 'crypt':
#         try:
#             import crypt
#         except ImportError:
#             raise ValueError('"crypt" password algorithm not supported in this environment')
#         return crypt.crypt(raw_password, salt)
#
#     if algorithm == 'md5':
#         return hashlib.md5(salt + raw_password).hexdigest()
#     elif algorithm == 'sha1':
#         return hashlib.sha1(salt + raw_password).hexdigest()
#     raise ValueError("Got unknown password algorithm type in password.")
#
#
# class Thumbnail(object):
#     @classmethod
#     def crear_thumbnail(cls, imagen=None, ruta='', ancho=None, alto=None):
#
#         THUMB_SIZE = 128, 128
#
#         if ancho and alto:
#             THUMB_SIZE = ancho, alto
#         elif ancho and not alto:
#             THUMB_SIZE = ancho, ancho
#         elif alto and not ancho:
#             THUMB_SIZE = alto, alto
#
# #             try:
# #                 image = Image.open(storage.open(imagen.name, 'r'))
# #             except Exception, e:
# #                 print e
# #                 return False
#         image = Image.open(StringIO(imagen.read()))
#
#         DJANGO_TYPE = image.format.lower()
#
#         if DJANGO_TYPE == 'jpeg':
#             PIL_TYPE = 'jpeg'
#             FILE_EXTENSION = 'jpg'
#         elif DJANGO_TYPE == 'png':
#             PIL_TYPE = 'png'
#             FILE_EXTENSION = 'png'
#         elif DJANGO_TYPE == 'gif':
#             PIL_TYPE = 'gif'
#             FILE_EXTENSION = 'gif'
#
#         image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
#
#         # Save thumbnail to in-memory file as StringIO
#         temp_thumb = StringIO()
#         image.save(temp_thumb, PIL_TYPE)
#         temp_thumb.seek(0)
#
#         suf = SimpleUploadedFile(ruta+imagen.name, temp_thumb.read(), content_type=DJANGO_TYPE)
#         # Load a ContentFile into the thumbnail field so it gets saved
# #             imagen.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
#         imagen.save(ruta+imagen.name, suf, save=False)
#         temp_thumb.close()
#         return True
# #         except Exception, e:
# #             print e
#
#


def handler_403(request,settings):
    from django.http import HttpResponseForbidden
    data = {'request': request, 'settings': settings, 'error': 'No tiene permisos suficientes para ver esta información.'}
    return HttpResponseForbidden(loader.render_to_string('403.html', data))

# # def cambio_moneda(valor=None,moneda_inicial=None,moneda_final=None):
# #     valor_final = 0.00
# #     #string_consulta = "http://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.xchange where pair in ('"+moneda_inicial+moneda_final+"')&env=store://datatables.org/alltableswithkeys&format=json"
# #     #resp = requests.get(string_consulta,headers={'Content-Type':'application/json'})
# #     #dict_respuesta = json.loads(resp.text)
# #     #tasa_cambio = dict_respuesta['query']['results']['rate']['Rate']
# #     tasa_cambio = get_tasa_cambio(moneda_inicial=moneda_inicial,moneda_final=moneda_final)
# #     valor_final = (valor * Decimal(tasa_cambio))
# #
# #     return valor_final
#
# # def get_tasa_cambio(moneda_inicial=None,moneda_final=None):
# #     import json,requests
# #     string_consulta = "http://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.xchange where pair in ('"+moneda_inicial+moneda_final+"')&env=store://datatables.org/alltableswithkeys&format=json"
# #     resp = requests.get(string_consulta,headers={'Content-Type':'application/json'})
# #     dict_respuesta = json.loads(resp.text)
# #     tasa_cambio = dict_respuesta['query']['results']['rate']['Rate']
# #     return tasa_cambio
#
#
# def get_dias_laborales(fecha_inicio, fecha_fin):
#     it_date = fecha_inicio
#     lista_fechas = []
#     while(it_date <= fecha_fin):
#         lista_fechas.append(it_date)
#         it_date = it_date+timedelta(hours=24)
#
#     num_dias_fines_de_semana = 0
#     for f in lista_fechas:
#         if f.weekday() in [5,6]:
#             num_dias_fines_de_semana+=1
#
#     dias_laborales = (fecha_fin-fecha_inicio).days - num_dias_fines_de_semana
#     return dias_laborales
#
#
# def get_fines_de_semana(fecha_inicio, fecha_fin):
#     it_date = fecha_inicio
#     lista_fechas = []
#     while(it_date <= fecha_fin):
#         lista_fechas.append(it_date)
#         it_date = it_date+timedelta(hours=24)
#
#     num_dias_fines_de_semana = 0
#     for f in lista_fechas:
#         if f.weekday() in [5,6]:
#             num_dias_fines_de_semana+=1
#
#     return num_dias_fines_de_semana
#
#
# def diff_minutos(fecha_inicio, fecha_fin):
#
#     fmt = '%Y-%m-%d %H:%M:%S'
#     d1 = datetime.strptime(fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'), fmt)
#     d2 = datetime.strptime(fecha_fin.strftime('%Y-%m-%d %H:%M:%S'), fmt)
#
#     diff = d2 - d1
#     diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
#
#     return diff_minutes
#
#
# # ____________ archivos ____________
#
#
# def combine_chunks(total_parts, total_size, source_folder, dest):
#     """ Combine a chunked file into a whole file again. Goes through each part
#     , in order, and appends that part's bytes to another destination file.
#     Chunks are stored in media/chunks
#     Uploads are saved in media/uploads
#     """
#
#     if not os.path.exists(os.path.dirname(dest)):
#         os.makedirs(os.path.dirname(dest))
#
#     with open(dest, 'wb+') as destination:
#         for i in xrange(total_parts):
#             part = os.path.join(source_folder, str(i))
#             with open(part, 'rb') as source:
#                 destination.write(source.read())
#
#
# def save_upload(f, path):
#     """ Save an upload. Django will automatically "chunk" incoming files
#     (even when previously chunked by fine-uploader) to prevent large files
#     from taking up your server's memory. If Django has chunked the file, then
#     write the chunks, otherwise, save as you would normally save a file in
#     Python.
#     Uploads are stored in media/uploads
#     """
#     if not os.path.exists(os.path.dirname(path)):
#         os.makedirs(os.path.dirname(path))
#
#     with open(path, 'wb+') as destination:
#         if hasattr(f, 'multiple_chunks') and f.multiple_chunks():
#             for chunk in f.chunks():
#                 destination.write(chunk)
#         else:
#             destination.write(f.read())
#
#
# def handle_upload(f, fileattrs, directory_upload, directory_chunks):
#     """ Handle a chunked or non-chunked upload.
#     """
#     logger.info(fileattrs)
#
#     chunked = False
#     dest_folder = os.path.join(directory_upload, fileattrs['qquuid'])
#     dest = os.path.join(dest_folder, fileattrs['qqfilename'])
#
#     # Chunked
#     if fileattrs['qqtotalparts'] and int(fileattrs['qqtotalparts']) > 1:
#         chunked = True
#         dest_folder = os.path.join(directory_chunks, fileattrs['qquuid'])
#         dest = os.path.join(dest_folder, fileattrs['qqfilename'], str(fileattrs['qqpartindex']))
#         logger.info('Chunked upload received')
#
#     save_upload(f, dest)
#     logger.info('Upload saved: %s' % dest)
#
#     # If the last chunk has been sent, combine the parts.
#     if chunked and (fileattrs['qqtotalparts'] - 1 == fileattrs['qqpartindex']):
#
#         logger.info('Combining chunks: %s' % os.path.dirname(dest))
#         combine_chunks(fileattrs['qqtotalparts'],
#             fileattrs['qqtotalfilesize'],
#             source_folder=os.path.dirname(dest),
#             dest=os.path.join(directory_upload, fileattrs['qquuid'], fileattrs['qqfilename']))
#         logger.info('Combined: %s' % dest)
#
#         shutil.rmtree(os.path.dirname(os.path.dirname(dest)))
#
#
# def handle_deleted_file(uuid,upload_directory):
#     """ Handles a filesystem delete based on UUID."""
#     # logger.info(uuid)
#
#     loc = os.path.join(upload_directory, uuid)
#     shutil.rmtree(loc)
#
#
# def disminuir_peso_imagen(ruta_completa_archivo,calidad=75):
#     """
#     Disminuye el peso de una imagen data la ruta completa y la calidad de imagen.
#     :param ruta_completa_archivo:
#     :param calidad:
#     :return:
#     """
#     from PIL import Image
#     import StringIO
#     from django.core.files.uploadedfile import InMemoryUploadedFile
#
#     nombre_archivo_imagen = ruta_completa_archivo.split('/')[-1]
#
#     # abro imagen
#     imagenx = Image.open(ruta_completa_archivo)
#
#     extension = nombre_archivo_imagen.split('.')[1]
#
#     if extension == 'png':
#         # Pongo fondo de blanco para eliminar la transparencia en caso que venga como PNG
#         fondo_blanco = Image.new("RGB", imagenx.size, (255,255,255))
#         fondo_blanco.paste(imagenx,imagenx)
#
#         # empato con la misma variable de la imagen con fondo blanco
#         imagenx  = fondo_blanco
#
#     # imagenx.thumbnail((640,480), Img.ANTIALIAS)
#     output = StringIO.StringIO()
#     imagenx = imagenx.convert('RGB')
#     imagenx.save(output, format='JPEG', quality=calidad)
#     output.seek(0)
#     return InMemoryUploadedFile(output,'ImageField', "%s" % nombre_archivo_imagen, 'image/jpeg', output.len, None)
#
#
# def remover_caracteres_especiales(cadena=None):
#     cadena = smart_str(cadena).replace('Ñ', 'N').replace('ñ', 'n').replace('&','&amp;').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U').replace('à','a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u').replace('½','1/2').replace('ü','u').replace('À','A').replace('Ç','C').replace('È','E').replace('Ì','I').replace('Ò','O').replace('Ù','U').replace("`",'').replace("´",'').replace("'",'')
#     return cadena
#
#
# def escapar_caracteres_especiales(cadena):
#     cadena = remover_caracteres_especiales(cadena)
#     cadena = (c for c in cadena if 0 < ord(c) < 127)
#     return ''.join(cadena)
#
#
# def procesar_nombre_con_secuencial(nombre_archivo,secuencial):
#     nombre_archivo,extension = os.path.splitext(nombre_archivo)
#     cadena_procesada = (nombre_archivo)+'_'+str(secuencial)+extension
#     return cadena_procesada
#
#
# def timesince_between_dates(d1,d2):
#     from dateutil.relativedelta import relativedelta
#     rd = relativedelta(d2,d1)
#     dict_timesince = rd.__dict__
#     return dict_timesince
#
#
# def timesince_between_dates_string(d1,d2):
#     dict = timesince_between_dates(d1,d2)
#     valor = "%(years)d año(s), %(months)d mes(es), %(days)d día(s)" % dict
#     return valor
#
#
# def validar_cedula(cedula):
#     try:
#         valores = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
#         suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
#         if int(cedula[9]) == 0:
#             if int(str(suma)[-1:]) == 0:
#                 return True
#             else:
#                 return False
#         return int(cedula[9]) == 10 - int(str(suma)[-1:])
#     except Exception:
#         return False
#
#
def get_or_none(model, *args, **kwargs):
    # if **kwargs == None:
    #     return None
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
#
#
# def diferencia_diccionarios(diccionario_primero, diccionario_segundo):
#     KEYNOTFOUNDIN1 = '<KEYNOTFOUNDIN1>'  # KeyNotFound for dictDiff
#     KEYNOTFOUNDIN2 = '<KEYNOTFOUNDIN2>'  # KeyNotFound for dictDiff
#
#     """ Return a dict of keys that differ with another config object.  If a value is
#         not found in one fo the configs, it will be represented by KEYNOTFOUND.
#         @param first:   Fist dictionary to diff.
#         @param second:  Second dicationary to diff.
#         @return diff:   Dict of Key => (first.val, second.val)
#     """
#     diff = {}
#     sd1 = set(diccionario_primero)
#     sd2 = set(diccionario_segundo)
#     #Keys missing in the second dict
#     for key in sd1.difference(sd2):
#         diff[key] = KEYNOTFOUNDIN2
#     #Keys missing in the first dict
#     for key in sd2.difference(sd1):
#         diff[key] = KEYNOTFOUNDIN1
#     #Check for differences
#     for key in sd1.intersection(sd2):
#         if diccionario_primero[key] != diccionario_segundo[key]:
#             diff[key] = (diccionario_primero[key], diccionario_segundo[key])
#     return diff
#
# def currency(value):
#     if value not in (None, ''):
#         locale.setlocale(locale.LC_ALL, settings.LOCALE_ALL_CONFIG)
#         locale.setlocale(locale.LC_NUMERIC, settings.LOCALE_NUMERIC_CONFIG)
#         locale.setlocale(locale.LC_MONETARY, settings.LOCALE_NUMERIC_CONFIG)
#         return locale.currency(value, grouping=True)
#
#
# def keys_exists(element, *keys):
#     '''
#     Check if *keys (nested) exists in `element` (dict).
#     '''
#     if type(element) is not dict:
#         raise AttributeError('keys_exists() expects dict as first argument.')
#     if len(keys) == 0:
#         raise AttributeError('keys_exists() expects at least two arguments, one given.')
#
#     _element = element
#     for key in keys:
#         try:
#             _element = _element[key]
#         except KeyError:
#             return False
#     return True
#
#
# def deEmojify(inputString):
#     """Remueve los emojies de un string"""
#     return inputString.encode('ascii', 'ignore').decode('ascii')
#
#
# def remover_acentos(texto):
#     """Remueve los acentos(tildes) de un texto"""
#     try:
#         texto = unicode(texto, 'utf-8')
#     except NameError:
#         pass
#     texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode("utf-8")
#     return str(texto)

# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
    # setup file paths variable
    filePaths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)

    # return all paths
    return filePaths


# Declare the main function
def obtener_firmados_zip(dir_name):
    # Assign the name of the directory to zip
    # dir_name = 'mydir'

    # Call the function to retrieve all files and folders of the assigned directory
    filePaths = retrieve_file_paths(dir_name)

    # printing the list of all files to be zipped
    # print('The following list of files will be zipped:')
    # for fileName in filePaths:
    #     print(fileName)

    # writing files to a zipfile
    zip_file = zipfile.ZipFile(dir_name + '.zip', 'w')
    with zip_file:
        # writing each file one by one
        for file in filePaths:
            zip_file.write(file)

def procesar_nombre_archivo(nombre): #genera codigo a partir del nombre del modelo
    chars = {'j', 'a', 'v', 'g', 'k', 'p',
             'r', '1', 'i', 'c', '6',
             'n', 'y', '2', '9', 'b', 'x', 'f', 'u', '7', 'z', 'l', 'e',
             'w', 'q', 't', 'd', '8', '3', '0', 'h', 's', '4', 'm', ' ',
             'X', 'o', '5'}
    nombre = nombre.lower()
    # nombre = unidecode.unidecode(nombre)
    codigo =([word for word in nombre if all(char in chars for char in word)])
    cod = ''.join(codigo)
    cod = cod.replace(' ', '_')
    cod = cod[0:-3]+'.pdf'
    return cod

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def remover_acentos(texto):
    """Remueve los acentos(tildes) de un texto"""
    if not isinstance(texto, unicode):
        try:
            texto = unicode(texto, 'utf-8')
        except NameError:
            pass
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode("utf-8")
    return str(texto)


def remover_caracteres_especiales_texto(texto, espacios=False, acentos=False, admitidos_char_list=None, rechazados_char_list=None):
    """Remueve todos los caracteres especiales de un string"""
    letras_minus    = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    letras_mayus    = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numeros         = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # tildes         = ['á','é','í','ó','ú','Á','É','Í','Ó','Ú']

    if espacios:  # si el texto tiene espacios, se agrega a la lista de caracteres admitidos
        admitidos_char_list = admitidos_char_list + [' '] if admitidos_char_list else [' ']

    if not acentos:  # cambia los caracteres acentuados, por sus equivalentes sin acento
        texto = remover_acentos(texto)

    # Agrega y elimina los caracteres validos de acuerdo a lo que llega en la funcion
    caracteres_admitidos = letras_minus + letras_mayus + numeros
    caracteres_admitidos = caracteres_admitidos + admitidos_char_list if admitidos_char_list else caracteres_admitidos
    caracteres_admitidos = [c for c in caracteres_admitidos if c not in rechazados_char_list] if rechazados_char_list else caracteres_admitidos

    texto_limpio = ([word for word in texto if all(char in caracteres_admitidos for char in word)])
    texto_limpio = ''.join(texto_limpio)  # Cast to string

    return texto_limpio

def copiar_directorio(origen,destino):
    shutil.copytree(origen, destino)

def copiar_archivos(origen,destino,prefijo=""):
    root_path=origen
    os.mkdir(destino)
    for root, subdirs, files in os.walk(root_path):
        # print('--\nroot = ' + root)
        # for subdir in subdirs:
        #     # print('\t- subdirectory ' + subdir)
        #     pass

        for filename in files:
            file_path = os.path.join(root, filename)
            fdir, fname = os.path.split(file_path)
            new_name=prefijo+fname

            # print(new_name)
            file_destino= os.path.join(destino,new_name)
            # print(file_path)
            # print(file_destino)
            shutil.copy(file_path,file_destino)

def kbytes_to_mb(cantidad_bytes):
    return float(cantidad_bytes/1000)

def timestamp():
    return str(int(time.time()))


def print_exception_line():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    # print(exc_type, fname, exc_tb.tb_lineno)

def remover_caracteres_especiales(cadena=None):
    cadena = smart_str(cadena).replace('Ñ', 'N').replace('ñ', 'n').replace('&','&amp;').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U').replace('à','a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u').replace('½','1/2').replace('ü','u').replace('À','A').replace('Ç','C').replace('È','E').replace('Ì','I').replace('Ò','O').replace('Ù','U').replace("`",'').replace("´",'').replace("'",'')
    return cadena
