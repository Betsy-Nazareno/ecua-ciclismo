from django.contrib import admin
from django import forms

from ecuaciclismo.apps.backend.ruta.models import Requisito, EtiquetaRuta, Colaboracion, GrupoEncuentro


class ColaboracionForm(forms.ModelForm):
    class Meta:
        model = Colaboracion
        fields = ('nombre',)

class RequisitoForm(forms.ModelForm):
    class Meta:
        model = Requisito
        fields = ('nombre',)

class EtiquetaRutaForm(forms.ModelForm):
    class Meta:
        model = EtiquetaRuta
        fields = ('nombre',)

class GrupoEncuentroForm(forms.ModelForm):
    class Meta:
        model = GrupoEncuentro
        fields = ('nombre',)

class ColaboracionAdmin(admin.ModelAdmin):
    modal = Colaboracion
    form = ColaboracionForm
    search_fields = ['nombre']
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    title = 'Colaboraciones ruta'

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()

class RequisitoAdmin(admin.ModelAdmin):
    modal = Requisito
    form = RequisitoForm
    search_fields = ['nombre']
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    title = 'Requisitos ruta'

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

class GrupoEncuentroAdmin(admin.ModelAdmin):
    modal = GrupoEncuentro
    form = GrupoEncuentroForm
    search_fields = ['nombre']
    list_display = ('nombre',)
    list_display_links = ('nombre',)
    title = 'Grupo encuentro'

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()

admin.site.register(Colaboracion, ColaboracionAdmin)
admin.site.register(Requisito, RequisitoAdmin)
admin.site.register(EtiquetaRuta, EtiquetaRutaAdmin)
admin.site.register(GrupoEncuentro, GrupoEncuentroAdmin)