from django.contrib.auth.models import User
from django.db import models

from ecuaciclismo.apps.backend.lugar.models import Local
from ecuaciclismo.apps.backend.solicitud.models import SolicitudVerificado, Solicitud
from ecuaciclismo.apps.backend.usuario.models import DetalleUsuario

class UsuarioNegocio(User):
    """
    Modelo proxy que envuelve todos los metodos relacionados con los usuarios dueños de negocios.
    """
    
    class Meta:
        proxy = True
        
    @property
    def negocio(self) -> Local:
        return Local.objects.filter(user=self).first()
    
    @property
    def detalles(self) -> DetalleUsuario:
        return DetalleUsuario.objects.filter(usuario=self).first()
        
    def save(self):
        """
        Sobreescritura del metodo save. 
        Este adjunta un negocio en caso de que el usuario sea nuevo, asimismo adjunta sus respectivos detalles
        """
        
        es_nuevo = self.pk is None
        super().save()
        
        if es_nuevo:
            self._crear_detalle_usuario()
            self._asociar_negocio_vacio()
            self._crear_solicitud()
        
    def _crear_detalle_usuario(self):
        detalle = DetalleUsuario(
            usuario=self,
            isPropietary=True,
        )
        detalle.save()
        
        return detalle
    
    def _asociar_negocio_vacio(self):
        local = Local(
            user= self,
            ubicacion=None,
            isActived=False,
            descripcion='',
            nombre=''
        )
        local.save()
        
        return local
    
    def _crear_solicitud(self):
        Solicitud(
            user=self,
            estado='Pendiente'
        ).save()
    
    