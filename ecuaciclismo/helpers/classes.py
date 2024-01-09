# coding=utf-8
# django
import base64
import os
import time
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage

from mimetypes import guess_type
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

class MensajeCorreoElectronico(object):

    @classmethod
    def get_mensaje_conexion(cls, titulo, contenido, correos_destinatarios, empresa, correos_en_copia=None,
                             correo_para_respuesta=None, bcc=settings.EMAIL_DEVELOPER):


        configuracion_correo_notificacion = empresa.get_configuracion_correo_notificaciones_validando()

        correo_developer = []
        correo_developer.append(bcc)

        lista_correo_para_respuesta = []
        if correo_para_respuesta == None:
            lista_correo_para_respuesta.append(configuracion_correo_notificacion.server_email)
        else:
            lista_correo_para_respuesta.append(correo_para_respuesta)

        con = mail.get_connection(host=configuracion_correo_notificacion.smtp_host,
                                  username=configuracion_correo_notificacion.server_email,
                                  password=configuracion_correo_notificacion.email_host_password)
        message = EmailMessage(subject=titulo, body=contenido, to=correos_destinatarios, cc=correos_en_copia,
                               from_email=configuracion_correo_notificacion.server_email, bcc=correo_developer,
                               reply_to=lista_correo_para_respuesta, connection=con)
        message.content_subtype = "html"

        return message

    @classmethod
    def get_mensaje_conexion2(cls, titulo, contenido, correos_destinatarios, empresa=None, correos_en_copia=None,
                              correo_para_respuesta=None, bcc=settings.EMAIL_DEVELOPER, attachment=None):

        from ecuaciclismo.helpers.tools_utilities import get_or_none

        configuracion_correo_notificacion = {'server_email': settings.SERVER_EMAIL,
                                                 'smtp_host': settings.EMAIL_HOST,
                                                 'smtp_port': settings.EMAIL_PORT,
                                                 'email_host_user': settings.EMAIL_HOST_USER,
                                                 'email_host_password': settings.EMAIL_HOST_PASSWORD}

        correo_developer = []
        correo_developer.append(bcc)

        lista_correo_para_respuesta = []
        if correo_para_respuesta == None:
            lista_correo_para_respuesta.append(configuracion_correo_notificacion['server_email'])
        else:
            lista_correo_para_respuesta.append(correo_para_respuesta)


        con = mail.get_connection(host=configuracion_correo_notificacion['smtp_host'],
                                  username=configuracion_correo_notificacion['server_email'],
                                  password=configuracion_correo_notificacion['email_host_password'])

        message = EmailMessage(subject=titulo, body=contenido, to=correos_destinatarios, cc=correos_en_copia,
                               from_email=configuracion_correo_notificacion['server_email'], bcc=correo_developer,
                               reply_to=lista_correo_para_respuesta, connection=con,  headers={'From': 'Ecuaciclismo <'+configuracion_correo_notificacion['server_email']+'>'})
        message.content_subtype = "html"

        if attachment:
            filename = attachment.split('/')[-1]
            mimetype, encoding = guess_type(attachment)
            mimetype = mimetype.split('/', 1)
            fp = open(attachment, 'rb')
            attachment = MIMEBase(mimetype[0], mimetype[1])
            attachment.set_payload(fp.read())
            fp.close()
            encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment',
                                  filename=os.path.basename(filename))
            message.attach(attachment)

        return message
