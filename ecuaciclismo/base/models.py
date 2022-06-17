# coding=utf-8
# django
import io
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.encoding import smart_str


from django.template.loader import get_template
from datetime import date, datetime

from ecuaciclismo.helpers.models import ModeloBase
from ecuaciclismo.helpers.tools_utilities import email_embed_image, email_embed_logos, get_or_none
from ecuaciclismo.helpers.xlsxwriter_styles import cargarFormatos


class LogActividad(models.Model):
    """ Modelo que almacena las actividades de los usuarios realizadas en el sistema"""
    ACCION_CREO     = 'CR'
    ACCION_MODIFICO = 'MO'
    ACCION_CONSULTA = 'CO'
    ACCION_ELIMINO  = 'EL'

    ACCION_CHOICES = ((ACCION_CREO,     'Creación'),
                      (ACCION_MODIFICO, 'Modificación'),
                      (ACCION_CONSULTA, 'Consulta'),
                      (ACCION_ELIMINO,  'Eliminación'))

    fecha_hora  = models.DateTimeField(auto_now_add=True)
    usuario     = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    accion      = models.CharField(max_length=2, choices=ACCION_CHOICES)
    descripcion = models.TextField()
    data        = models.TextField(null=True)  # en desarrollo
    # empresa     = models.ForeignKey('empresa.Empresa', null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ('-fecha_hora', '-id')

    def __str__(self):
        return self.descripcion

#     @classmethod
#     def exportar_excel(cls, logs=None):
#         from xlsxwriter.workbook import Workbook
#         output = io.BytesIO()
#         workbook = Workbook(output)
#         diccionario_formatos_xlsxwriter = cargarFormatos(workbook)
#
#         worksheet = workbook.add_worksheet("Reporte")
#
#         worksheet.merge_range('A1:D1', 'LOGS DE ACTIVIDADES', diccionario_formatos_xlsxwriter['titulo_reporte'])
#         worksheet.merge_range('A2:D2', 'Fecha : %s' % (datetime.now().strftime("%d/%m/%Y")), diccionario_formatos_xlsxwriter['subtitulo_centrado'])
#         worksheet.set_column('A:A', 20)
#         worksheet.set_column('B:B', 30)
#         worksheet.set_column('C:C', 20)
#         worksheet.set_column('D:D', 40)
#
#         fila = 3
#         i = 0
#         worksheet.write(fila, i, 'FECHA', diccionario_formatos_xlsxwriter['subtitulo_centrado'])
#         i += 1
#         worksheet.write(fila, i, 'USUARIO', diccionario_formatos_xlsxwriter['subtitulo_centrado'])
#         i += 1
#         worksheet.write(fila, i, 'ACCIÓN', diccionario_formatos_xlsxwriter['subtitulo_centrado'])
#         i += 1
#         worksheet.write(fila, i, 'DESCRIPCIÓN', diccionario_formatos_xlsxwriter['subtitulo_centrado'])
#         i += 1
#
#         fila += 1
#         for log in logs:
#             i = 0
#             worksheet.write(fila, i, log.fecha_hora.strftime('%d/%m/%Y %H:%M'), diccionario_formatos_xlsxwriter['normal'])
#             i += 1
#             worksheet.write(fila, i, smart_str(log.usuario.get_full_name()) + '(' + smart_str(log.usuario) + ')', diccionario_formatos_xlsxwriter['normal'])
#             i += 1
#             worksheet.write(fila, i, log.get_accion_display(), diccionario_formatos_xlsxwriter['normal'])
#             i += 1
#             worksheet.write(fila, i, log.descripcion, diccionario_formatos_xlsxwriter['normal'])
#             i += 1
#             fila += 1
#         workbook.close()
#         output.seek(0)
#         return output.read()
#
#
class RegistroCambiarClave(models.Model):
    usuario     = models.ForeignKey(User, on_delete=models.PROTECT)
    token       = models.CharField(max_length=50)

    def enviar(self, nombre_imagen_notificacion = 'user-reset-password.png'):
        from ecuaciclismo.helpers.classes import MensajeCorreoElectronico

        if settings.ENVIAR_NOTIFICACIONES_EMAIL_GLOBAL:
            my_url = settings.HTTP + settings.URLC + '/web_app/'+'reset-password/'+str(self.token)+'/'
            contenido = get_template('email_templates/email_notificacion.html').render({
                'titulo': 'Comextweb Aaranceles: Recuperación de Contraseña',
                'mensaje': 'Hemos recibido su solicitud',
                'empresa': '',
                'tipo': 'cambio de contraseña',
                "cuerpo": "Hola " + self.usuario.first_name + ", para restablecer su contraseña por favor ingrese al siguiente enlace:",
                'descripcion_boton': 'Restablecer',
                'url': my_url
            })
            msg = MensajeCorreoElectronico.get_mensaje_conexion2(titulo='Comextweb Aranceles: Recuperación de Contraseña',contenido=contenido, correos_destinatarios=[self.usuario.email])
            # email_embed_image(msg, 'logo-empresa',
            #                   open('%sstatic/email_images/signatur-e.png' % settings.STATIC_ROOT,
            #                        'rb').read())
            # email_embed_logos(msg)
            try:
                import _thread
                _thread.start_new_thread(msg.send, ())
                # msg.send()
            except Exception as e:
                pass
                # print(e)

    @classmethod
    def verificarToken(cls, token_publico=None):
        try:
            registro = get_or_none(RegistroCambiarClave, token=token_publico)
            if registro:
                return True
            else:
                return False

        except ObjectDoesNotExist:
            return False

        except Exception:
            return False

# class ImagenTemporal(models.Model):
#     archivo     = models.FileField(upload_to='tmp/img', null=True, default=None)
#
#     def get_hash(self):
#         import hashids
#         hash = hashids.Hashids(salt=settings.SEMILLA_ARCHIVOS_TEMPORALES).encode(self.id,0,0)
#         return hash
#
#     def reversar(self):
#         ruta_fisica_archivo = os.path.join(settings.MEDIA_ROOT, str(self.archivo))
#         if os.path.exists(ruta_fisica_archivo):
#             os.remove(ruta_fisica_archivo)
#
#     def delete(self):
#         self.reversar()
#         ModeloBase.delete(self)
