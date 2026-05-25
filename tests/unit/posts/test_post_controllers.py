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

    # 2. MONKEYPATCH CORREGIDO: Interceptamos el servicio tal y como lo importa tu "controllers.py"
    # Nota: Como controllers.py hace 'from src.services.post_service import PostService', 
    # mockeamos el destino final donde se ejecuta en el controlador.
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