# coding=utf-8
from django import forms

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario', 'icon-feedback':'icon-user'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'icon-feedback':'icon-lock2'}))

    def clean_username(self):
        return self.cleaned_data['username']

    def clean_password(self):
        return self.cleaned_data['password']


class ConsultarLogForm(forms.Form):
    filtro = forms.CharField(required=False,max_length = 40, widget = forms.TextInput(attrs = {'class': 'form-control input-sm '}))
    usuario = forms.ModelChoiceField(User.objects.filter(),widget=forms.widgets.Select({'class': 'form-control input-sm '}), empty_label='Seleccione usuario',required=False)
    fecha_emision_desde = forms.DateTimeField(input_formats = ('%d/%m/%Y %H:%M',), required = False, widget = forms.DateTimeInput(attrs = {'class':'form-control input-sm datetimepicker '}))
    fecha_emision_hasta = forms.DateTimeField(input_formats = ('%d/%m/%Y %H:%M',), required = False, widget = forms.DateTimeInput(attrs = {'class':'form-control input-sm datetimepicker'}))


class SolicitarCambioClaveForm(forms.Form):
    parametro = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control input-sm '}))

    def clean_parametro(self):
        """ Se busca un email o usuario por el parametro ingresado """
        from django.contrib.auth.models import User
        from django.db.models import Q
        parametro = self.cleaned_data.get('parametro')
        try:
            usuario = User.objects.get(Q(username=parametro) | Q(email=parametro))
            return usuario
        except User.DoesNotExist:
            raise forms.ValidationError(u"Clave o correo eléctronico incorrecto.")
        return parametro

    def save(self):
        """ Guarda un registro de solicitud de clave """
        import uuid
        from ecuaciclismo.base.models import RegistroCambiarClave
        registro = RegistroCambiarClave(usuario=self.cleaned_data['parametro'])
        registro.token = str(uuid.uuid4())
        registro.save()
        return registro


class ProcesarCambioClaveOlvidadaForm(forms.Form):
    token                       = forms.CharField(widget=forms.HiddenInput(), required=False)
    clave_nueva                 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva clave'}), max_length=20)
    confirmacion_clave_nueva    = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar clave'}), max_length=20)

    def __init__(self, data=None, prefix=None, initial=None, usuario=None):
        if not usuario: raise Exception('El formulario debe contener el usuario')
        self.usuario = usuario
        super(ProcesarCambioClaveOlvidadaForm, self).__init__(data=data, prefix=prefix, initial=initial)

    def clean(self):
        clave_nueva = self.cleaned_data.get('clave_nueva')
        confirmacion_clave_nueva = self.cleaned_data.get('confirmacion_clave_nueva')
        if clave_nueva and confirmacion_clave_nueva and clave_nueva != confirmacion_clave_nueva:
            raise forms.ValidationError(u"La confirmación y la nueva clave deben ser iguales")
        return self.cleaned_data

    def save(self):
        """ Guarda la nueva contraseña del usuario. """
        self.usuario.set_password(self.cleaned_data['clave_nueva'])
        self.usuario.save()
        return self.usuario
