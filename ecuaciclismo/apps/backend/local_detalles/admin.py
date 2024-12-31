from django.contrib import admin

from .models import *

class ProductosAdmin(admin.ModelAdmin):
    list_display = ( 'nombre', 'descripcion', 'fecha_creacion' )
    fields = [ 'nombre', 'descripcion' ]

class ServiciosAdicionalesAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'nombre', 'fecha_creacion' )
    fields = [ 'nombre' ]
    
admin.site.register(Producto, ProductosAdmin)
admin.site.register(ServicioAdicional, ServiciosAdicionalesAdmin)
