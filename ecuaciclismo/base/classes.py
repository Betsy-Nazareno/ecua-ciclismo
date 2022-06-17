# coding=utf-8
from hashids import Hashids


# class UtilPermisox(object):
#
#     def __init__(self, empresa, usuario):
#         """ Constructor, inicializa los atributos del objeto """
#         self.empresa = empresa
#         self.usuario = usuario
#         self.dict = {}
#
#     def __getattr__(self, permiso):
#         try:
#             if self.usuario.is_superuser:#Si es Super Usuario siempre retorno True
#                 return True
#             valor = self.dict.get(permiso)
#             if valor!=None:
#                 return valor
#             else:
#                 try:
#                     from ecuaciclismo.apps.backend.usuario.models import RolUsuario,PermisoRol
#                     roles = RolUsuario.objects.filter(empresa_usuario=self.usuario,rol__empresa=self.empresa).values_list('rol_id',flat=True)
#                     permiso_usuario_rol = PermisoRol.objects.filter(permiso__permiso=permiso,rol__id__in=roles,acceso=True).first()#acceso
#                     val = permiso_usuario_rol.acceso
#                     self.dict[permiso] = val
#                     return val
#                 except Exception as e:
#                     return None
#         except KeyError:
#             msg = "'{0}' object has no attribute '{1}'"
#             raise AttributeError(msg.format(type(self).__name__, permiso))
