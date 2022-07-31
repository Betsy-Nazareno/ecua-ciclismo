from django.contrib import admin
from django import forms

from ecuaciclismo.apps.backend.ruta.models import Requisito, EtiquetaRuta


class RequisitoForm(forms.ModelForm):
    class Meta:
        model = Requisito
        fields = ('nombre',)

class EtiquetaRutaForm(forms.ModelForm):
    class Meta:
        model = EtiquetaRuta
        fields = ('nombre',)

class RequisitoAdmin(admin.ModelAdmin):
    modal = Requisito
    form = RequisitoForm
    search_fields = ['nombre']
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    title = 'Requisitos'

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()

class EtiquetaRutaAdmin(admin.ModelAdmin):
    modal = EtiquetaRuta
    form = EtiquetaRutaForm
    search_fields = ['nombre']
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    title = 'Etiquetas ruta'

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()

admin.site.register(Requisito, RequisitoAdmin)
admin.site.register(EtiquetaRuta, EtiquetaRutaAdmin)