# Expansion del modulo Safepoint

## Estandares a seguir

### 1. Creación de modelos

Si se van a crear nuevos modelos colocarlos en la carpeta `ecuaciclismo/apps/backend/{caracteristica}` en donde {caracteristica} hace referencia a la razón o utilidad de ese modelo. Ejemplo:

- Se creará un modelo para categorias de productos de un negocio, entonces se crea el modelo en: `ecuaciclismo/apps/backend/negocios/models.py` y dentro de `models.py` podría ir:

```python

class Categoria(models.Model):
    ... # los campos del modelo

```

### 2. Funcionalidades

Para este proyecto de expansion se creará una nueva carpeta a la altura de la carpeta `backend/` (`ecuaciclismo/apps/backend/safepoint`).
En esta carpeta se colocaran todos los archivos de utilidades que se van a utilizar, siguiendo el estandar de colocar los archivos dentro de una carpeta que indique una caracteristica. Ejemplo:


```
├─── safepoint
│   │    📄 __init__.py
│   └─── 📁 autenticacion
│            📄 serializers.py
│            📄 services.py
│            📄 views.py
│            📄 __init__.py
```

Colocar todo el codigo referente a esa caracteristicas dentro de los archivos que corresponden.

### 3. Estandar de codigo

Procurar usar **Class Based Views** o **Viewset** con Django Rest Framework
- https://www.django-rest-framework.org/tutorial/3-class-based-views/
- https://www.django-rest-framework.org/api-guide/viewsets/
