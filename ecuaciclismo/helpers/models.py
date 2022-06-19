# coding=utf-8
#django
# from django.db.models.deletion import Collector
import datetime
import uuid

from django.conf import settings
from django.contrib.admin.utils import NestedObjects
from django.core import mail
from django.core.mail import EmailMessage
from django.db import models

# comextweb


class ModeloBase(models.Model):
    """ Modelo base para todos los modelos del ecuaciclismo """
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_cambio = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=100, null=True)

    def generar_token(self):
        token = str(uuid.uuid4())
        return token

    # def as_data(self):
    #     from ecuaciclismo.helpers.tools_utilities import remove_keys_endswidth
    #
    #     """ Devuelve una representación  del objeto parámetro como la data de un form """
    #     dic = self.__dict__.copy()
    #     remove_keys_endswidth(dic, '_cache')
    #     remove_keys_endswidth(dic, '_state')
    #     dic['pk'] = self._get_pk_val()
    #     for key in list(dic):
    #         if type(dic[key])== datetime.date:
    #             dic[key] = dic[key].strftime("%d/%m/%Y")
    #         if type(dic[key])== datetime.datetime:
    #             dic[key] = dic[key].strftime("%d/%m/%Y %H:%M")
    #         if len(key) > 3 and key[-3:] == '_id' and getattr(self, key[:-3]):
    #             dic[key[:-3]] = getattr(self, key[:-3])._get_pk_val()
    #             dic[key[:-3]+'_representacionff'] = str(getattr(self, key[:-3]))
    #
    #     return dic
    #
    # def can_delete(self):
    #     """ Método que verifica si el modelo puede ser eliminado """
    #     if self._get_pk_val():
    #         collector = NestedObjects(using="default") #database name
    #         collector.collect([self])
    #         if len(collector.data) > 1:
    #             list_relations = []
    #             for objeto in collector.data.keys():
    #                 name =( (str(objeto).split('.'))[-1])[:-2]
    #                 list_relations.append(name)
    #             # print(list_relations)
    #             # raise ApplicationError(u"Error! El registro tiene elementos asociados.  "+str(list_relations))
    #             raise
    #
    # def delete(self):
    #     """ Método para eliminar un registro """
    #     self.can_delete()
    #     models.Model.delete(self)
    #
    # def force_delete(self):
    #     """Elimina el objeto sin importar nada"""
    #     models.Model.delete(self)
    #
    # def save(self, **kwargs):
    #     """ Verifica que el objeto no haya sido modificado por otra sesión """
    #     if self.id:
    #         obj_db = self.__class__.objects.get(pk=self.id)
    #         # if obj_db.ultimo_cambio > self.ultimo_cambio:
    #         #     raise ApplicationError(u"El registro ha sido modificado por otra persona, por favor intente nuevamente.")
    #     models.Model.save(self)

    def save(self, **kwargs):
        if self.token is None or self.token == '':
            self.token = self.generar_token()
        models.Model.save(self)

    class Meta:
        abstract = True
