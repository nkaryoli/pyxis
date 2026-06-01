from types import SimpleNamespace
import pytest
from flask import Flask
from src.modules.posts.controllers import posts 

@pytest.fixture
def app():
    app_flask = Flask(__name__)
    app_flask.register_blueprint(posts)
    return app_flask

@pytest.fixture
def client(app):
    return app.test_client()



def test_listar_todos_api_ok(client, monkeypatch):
    """Comprueba que se listan todos los posts correctamente en formato JSON."""
    post_mock = SimpleNamespace(
        id_post=1,
        id_usuario=10,
        to_dict=lambda: {"id_post": 1, "titulo_post": "Test", "id_usuario": 10}
    )

    monkeypatch.setattr(
        "src.modules.posts.controllers.PostService.listar_todos",
        lambda: [post_mock]
    )

    response = client.get('/api/posts')
    
    assert response.status_code == 200
    assert response.is_json
    body = response.get_json()
    assert len(body) == 1
    assert body[0]["id_post"] == 1


def test_listar_todos_api_error_servidor(client, monkeypatch):
    """Comprueba que un error inesperado en el servicio devuelve un código 500."""
    def mock_error():
        raise Exception("Error interno en la base de datos")

    monkeypatch.setattr(
        "src.modules.posts.controllers.PostService.listar_todos",
        mock_error
    )

    response = client.get('/api/posts')
    body = response.get_json()

    assert response.status_code == 500
    assert response.is_json
    assert "Error interno" in body["error"]


def test_crear_post_api_ok(client, monkeypatch):
    """Comprueba que se puede crear un post enviando un JSON válido."""
    post_creado = SimpleNamespace(
        id_post=9,
        to_dict=lambda: {"id_post": 9, "titulo_post": "Nuevo Post", "id_usuario": 10}
    )

    monkeypatch.setattr(
        "src.modules.posts.controllers.UsuarioService.esta_matriculado",
        lambda id_usuario, codigo_modulo: True
    )

    monkeypatch.setattr(
        "src.modules.posts.controllers.PostService.crear_post",
        lambda titulo, contenido, id_usuario, codigo_modulo, imagen=None: post_creado
    )

    payload = {
        "titulo_post": "Nuevo Post",
        "contenido_post": "Contenido de un post de prueba",
        "id_usuario": 10,
        "codigo_modulo": "M06"
    }

    response = client.post('/api/posts', json=payload)
    body = response.get_json()

    assert response.status_code == 201
    assert response.is_json
    assert body["id_post"] == 9
    assert body["titulo_post"] == "Nuevo Post"




def test_ver_post_por_id_ok(client, monkeypatch):
    """Comprueba que se obtiene el post correcto si el ID existe."""
    post_mock = SimpleNamespace(
        id_post=5,
        to_dict=lambda: {"id_post": 5, "titulo_post": "Post Cinco"}
    )

    monkeypatch.setattr(
        "src.modules.posts.controllers.PostService.obtener_por_id",
        lambda id_post: post_mock if id_post == 5 else None
    )

    response = client.get('/api/posts/5')
    body = response.get_json()

    assert response.status_code == 200
    assert response.is_json
    assert body["id_post"] == 5


def test_ver_post_por_id_no_encontrado(client, monkeypatch):
    """Comprueba que devuelve 404 si el ID solicitado no existe."""
    monkeypatch.setattr(
        "src.modules.posts.controllers.PostService.obtener_por_id",
        lambda id_post: None
    )

    response = client.get('/api/posts/999')
    body = response.get_json()

    assert response.status_code == 404
    assert response.is_json
    assert "No se encontró ningún post con el ID 999" in body["error"]



def test_ver_posts_usuario_api_ok(client, monkeypatch):
    """Comprueba que se listan todos los posts asociados a un usuario específico."""
    post_mock = SimpleNamespace(
        id_post=1,
        id_usuario=10,
        to_dict=lambda: {"id_post": 1, "id_usuario": 10}
    )

    monkeypatch.setattr(
        "src.modules.posts.controllers.UsuarioService.obtener_posts_paginados",
        lambda id_usuario, page: ([post_mock.to_dict()], 1)
    )

    response = client.get('/api/usuarios/10/posts')
    body = response.get_json()

    assert response.status_code == 200
    assert len(body["items"]) == 1
    assert body["items"][0]["id_usuario"] == 10



def test_gestionar_post_sin_headers_autenticacion(client):
    """Comprueba que si faltan las cabeceras requeridas responde con 401 Unauthorized."""
    response = client.delete('/api/posts/1')
    body = response.get_json()

    assert response.status_code == 401
    assert "Autenticación requerida" in body["error"]


def test_modificar_post_autorizado_ok(client, monkeypatch):
    """Comprueba que el propietario puede actualizar un post mediante un método PUT."""
    post_mock = SimpleNamespace(id_post=1, id_usuario=10)
    post_actualizado = SimpleNamespace(
        id_post=1,
        to_dict=lambda: {"id_post": 1, "titulo_post": "Titulo Editado", "id_usuario": 10}
    )

    monkeypatch.setattr(
        "src.modules.posts.controllers.PostService.obtener_por_id",
        lambda id_post: post_mock
    )
    monkeypatch.setattr(
        "src.modules.posts.controllers.PostService.modificar_post",
        lambda *args, **kwargs: post_actualizado
    )

    headers = {'X-User-Id': '10', 'X-User-Role': 'ALUMNO'}
    payload = {"titulo_post": "Titulo Editado"}
    
    response = client.put('/api/posts/1', json=payload, headers=headers)
    body = response.get_json()

    assert response.status_code == 200
    assert body["titulo_post"] == "Titulo Editado"