from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ecuaciclismo.apps.backend.api.alerta.views import AlertaViewSet
from ecuaciclismo.apps.backend.api.bicicleta.views import BicicletaViewSet
from ecuaciclismo.apps.backend.api.consejodia.views import ConsejoDiaViewSet
from ecuaciclismo.apps.backend.api.lugar.views import LugarViewSet
from ecuaciclismo.apps.backend.api.publicacion.views import PublicacionViewSet
from ecuaciclismo.apps.backend.api.ruta.views import RutaViewSet
from ecuaciclismo.apps.backend.api.solicitud.views import SolicitudViewSet
from ecuaciclismo.apps.backend.api.usuario.views import UsuarioViewSet, DetalleUsuarioViewSet, \
    UsuarioRecuperarCredencialesViewSet
from ecuaciclismo.apps.backend.api.logs.views import CrearLogView

router = DefaultRouter()

# Registro de ViewSets
router.register(r'usuario', UsuarioViewSet)
router.register(r'detalleusuario', DetalleUsuarioViewSet)
router.register(r'consejodia', ConsejoDiaViewSet)
router.register(r'publicacion', PublicacionViewSet)
router.register(r'ruta', RutaViewSet)
router.register(r'alerta', AlertaViewSet)
router.register(r'lugar', LugarViewSet)
router.register(r'solicitud', SolicitudViewSet)
router.register(r'recuperar_credenciales', UsuarioRecuperarCredencialesViewSet)
router.register(r'logs', CrearLogView)
router.register(r'bicicleta', BicicletaViewSet)

# Aquí puedes agregar rutas adicionales que no estén directamente relacionadas con los ViewSets
url_patterns = [
    # Aquí se pueden registrar otras rutas específicas si es necesario
]

# Combina las rutas de `router` con las adicionales definidas en `url_patterns`
urlpatterns = router.urls + url_patterns
0