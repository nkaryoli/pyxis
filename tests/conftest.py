"""
Fixtures compartidas de pytest para el proyecto.

Coloca aquí fixtures comunes para que tanto tests unitarios como de
integración puedan reutilizarlas.

Fixtures proporcionadas:
- `app`: una instancia de la aplicación Flask creada con `create_app()` y
    configurada para testing (`TESTING=True`). Los tests pueden usarla para
    acceder a la configuración de la app o para crear fixtures dependientes.
- `client`: un `Flask.test_client()` que realiza llamadas HTTP internas
    (sin usar la red). Útil para tests de endpoints o integración que ejercitan
    las rutas.

Notas:
- El scope por defecto de las fixtures es `function`, por lo que cada test
    recibe una instancia limpia. Si necesitas compartir estado entre muchos
    tests (más lento), cambia el scope a `session`.
"""

import pytest
from src import create_app


@pytest.fixture
def app():
        """Crear y configurar una app Flask para testing.

        - Llama a la fábrica de la aplicación `create_app()` desde `src`.
        - Activa `TESTING` para que las excepciones lleguen al runner de tests y
            las extensiones (si las hay) se comporten en modo test.
        - Usamos `yield` para permitir añadir lógica de teardown después del test
            si hace falta.
        """
        app = create_app()
        app.config["TESTING"] = True
        yield app


@pytest.fixture
def client(app):
    """Devolver un cliente de pruebas para la app Flask.

    El cliente realiza peticiones contra la app sin arrancar un servidor
    HTTP real. Ejemplo de uso en un test::

        def test_index(client):
            resp = client.get('/')
            assert resp.status_code == 200

    """
    return app.test_client()