from types import SimpleNamespace
import pytest
from flask import Flask
# Ajusta esta ruta si tu blueprint de respuestas está en otra ubicación modular
from src.modules.respuestas.controllers import respuestas 

@pytest.fixture
def app():
    app_flask = Flask(__name__)
    app_flask.register_blueprint(respuestas)
    return app_flask

@pytest.fixture
def client(app):
    return app.test_client()


def test_crear_respuesta_api_ok(client, monkeypatch):
    """Comprueba que se puede crear una respuesta con datos válidos."""
    respuesta_mock = SimpleNamespace(
        id_respuesta=1,
        to_dict=lambda: {"id_respuesta": 1, "contenido_respuesta": "Buena solución", "id_usuario": 10}
    )

    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.crear_respuesta",
        lambda id_post, id_usuario, contenido, es_mejor, imagen: respuesta_mock
    )

    payload = {
        "contenido_respuesta": "Buena solución",
        "id_usuario": 10
    }

    response = client.post('/api/posts/5/respuestas', json=payload)
    body = response.get_json()

    assert response.status_code == 201
    assert response.is_json
    assert body["mensaje"] == "Respuesta creada con éxito"
    assert body["respuesta"]["id_respuesta"] == 1


def test_crear_respuesta_faltan_campos_obligatorios(client):
    """Comprueba que devuelve 400 si faltan datos requeridos en el JSON."""
    payload = {
        "id_usuario": 10
    }

    response = client.post('/api/posts/5/respuestas', json=payload)
    body = response.get_json()

    assert response.status_code == 400
    assert "Faltan campos obligatorios" in body["error"]



def test_listar_respuestas_post_api_ok(client, monkeypatch):
    """Comprueba que obtiene la lista de respuestas vinculadas a un post."""
    r_mock = SimpleNamespace(
        id_respuesta=1,
        to_dict=lambda: {"id_respuesta": 1, "id_post": 5}
    )

    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.obtener_respuestas_de_post",
        lambda id_post: [r_mock] if id_post == 5 else []
    )

    response = client.get('/api/posts/5/respuestas')
    body = response.get_json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["id_post"] == 5



def test_ver_respuestas_usuario_api_ok(client, monkeypatch):
    """Comprueba que obtiene las respuestas de un usuario específico."""
    r_mock = SimpleNamespace(
        id_respuesta=2,
        to_dict=lambda: {"id_respuesta": 2, "id_usuario": 44}
    )

    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.obtener_respuestas_de_usuario",
        lambda id_usuario: [r_mock] if id_usuario == 44 else []
    )

    response = client.get('/api/usuarios/44/respuestas')
    body = response.get_json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["id_usuario"] == 44


def test_gestionar_respuesta_sin_headers_da_401(client):
    """Comprueba la protección 401 si no se envían las cabeceras de rol."""
    response = client.delete('/api/respuestas/1')
    body = response.get_json()

    assert response.status_code == 401
    assert "Autenticación requerida" in body["error"]


def test_gestionar_respuesta_no_existente(client, monkeypatch):
    """Comprueba que da 404 si la respuesta solicitada no existe."""
    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.obtener_por_id",
        lambda id_respuesta: None
    )

    headers = {'X-User-Id': '10', 'X-User-Role': 'ALUMNO'}
    response = client.delete('/api/respuestas/999', headers=headers)
    body = response.get_json()

    assert response.status_code == 404
    assert "No se encontró ninguna respuesta con el ID 999" in body["error"]


def test_eliminar_respuesta_denegada_no_es_dueno(client, monkeypatch):
    """Comprueba que un ALUMNO no puede borrar la respuesta de otro usuario."""
    # La respuesta es del usuario 10
    respuesta_mock = SimpleNamespace(id_respuesta=1, id_usuario=10)

    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.obtener_por_id",
        lambda id_respuesta: respuesta_mock
    )

    headers = {'X-User-Id': '99', 'X-User-Role': 'ALUMNO'}
    response = client.delete('/api/respuestas/1', headers=headers)
    body = response.get_json()

    assert response.status_code == 403
    assert "No tienes permisos" in body["error"]


def test_eliminar_respuesta_autorizado_profesor(client, monkeypatch):
    """Comprueba que un PROFESOR puede borrar cualquier respuesta."""
    respuesta_mock = SimpleNamespace(id_respuesta=1, id_usuario=10)

    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.obtener_por_id",
        lambda id_respuesta: respuesta_mock
    )
    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.eliminar_respuesta",
        lambda id_respuesta: True
    )

    headers = {'X-User-Id': '55', 'X-User-Role': 'PROFESOR'}
    response = client.delete('/api/respuestas/1', headers=headers)
    body = response.get_json()

    assert response.status_code == 200
    assert body["mensaje"] == "Respuesta con ID 1精神 eliminada correctamente" or "eliminada correctamente" in body["mensaje"]


def test_modificar_respuesta_autorizado_propietario(client, monkeypatch):
    """Comprueba que el dueño de la respuesta puede modificarla exitosamente."""
    respuesta_mock = SimpleNamespace(id_respuesta=1, id_usuario=10)
    respuesta_editada = SimpleNamespace(
        id_respuesta=1,
        to_dict=lambda: {"id_respuesta": 1, "contenido_respuesta": "Texto cambiado"}
    )

    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.obtener_por_id",
        lambda id_respuesta: respuesta_mock
    )
    monkeypatch.setattr(
        "src.modules.respuestas.controllers.RespuestaService.modificar_respuesta",
        lambda id_respuesta, contenido, imagen: respuesta_editada
    )

    headers = {'X-User-Id': '10', 'X-User-Role': 'ALUMNO'}
    payload = {"contenido_respuesta": "Texto cambiado"}
    
    response = client.put('/api/respuestas/1', json=payload, headers=headers)
    body = response.get_json()

    assert response.status_code == 200
    assert body["mensaje"] == "Respuesta modificada con éxito"
    assert body["respuesta"]["contenido_respuesta"] == "Texto cambiado"