from django.contrib import admin

from .models import *

class TipoProductosAdmin(admin.ModelAdmin):
    list_display = ( 'nombre', 'descripcion', 'fecha_creacion' )
    fields = [ 'nombre', 'descripcion' ]

class ServicioDetalleAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'nombre', 'fecha_creacion' )
    fields = [ 'nombre' ]
    
admin.site.register(TipoProducto, TipoProductosAdmin)
admin.site.register(ServicioDetalle, ServicioDetalleAdmin)
