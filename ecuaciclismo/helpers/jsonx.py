# coding=utf-8
#from json import simplejson
import json
from django.http import HttpResponse
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.template import Template, Context
from decimal import Decimal
import datetime
 

class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        # TODO: los formatos de las fechas deben estar relacionados a settings
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%d/%m/%Y, %I:%M:%S %p')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%d/%m/%Y')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%I:%M %p')
        elif isinstance(obj, Decimal):
            return str(obj.__float__())
        return DjangoJSONEncoder.default(self, obj)

#falta testaer en este django 1.8 de comext
def jsonx(data):
    data = {"json_data": JSONEncoder(ensure_ascii=False).encode(data)}
    template = Template("{{json_data|safe}}")
    context = Context(data)
    return HttpResponse(template.render(context),
                        content_type="text/json-comment-filtered; charset=%s" % (settings.DEFAULT_CHARSET))
  
 
def json_string(data):
    return JSONEncoder(ensure_ascii=False).encode(data)

#falta testear en este django 1.8 de comext
# def string_to_json(s):
#     return simplejson.loads(s, encoding=settings.DEFAULT_CHARSET)
