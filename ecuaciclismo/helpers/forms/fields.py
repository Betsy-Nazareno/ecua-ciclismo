# coding=utf-8
from django.forms.fields import IntegerField
from django.forms.widgets import HiddenInput
# import json
import simplejson


class FinderField(IntegerField):
    widget = HiddenInput

    def __init__(self, klass=None, required=True, initial=None, **opts):
        self.klass = klass
        self.opts = opts
        IntegerField.__init__(self, required=required, initial=initial)

    def clean(self, value):
        value = IntegerField.clean(self, value)
        if value:
            instancia = self.klass.objects.get(pk=value)
            self.widget.attrs['representacionff'] = str(instancia)
            try:
                # self.widget.attrs['objdataff'] = json.dumps(instancia.as_data())
                self.widget.attrs['objdataff'] = simplejson.dumps(instancia.as_data())
            except AttributeError as e:
                pass
            return instancia
        return value

    def widget_attrs(self, widget):
        opts = self.opts and self.opts or {}
        # opts['class'] = 'object-hidden form-control'
        return opts
