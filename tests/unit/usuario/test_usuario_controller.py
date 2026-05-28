import pytest
from flask import Flask, g

# 1. Desactivar el decorador de autenticación antes de importar el blueprint
from src.services.auth_service import AuthService
AuthService.token_required = lambda f: f

# 2. MOCKEAR RENDER_TEMPLATE PARA EVITAR ERRORES DE JINJA2 (TemplateNotFound)
import flask
flask.render_template = lambda template_name_or_list, **context: f"Rendered {template_name_or_list}"

# 3. Importar desde tu estructura modular real
from src.modules.usuario.controllers import usuarios_bp
from src.services.usuario_service import UsuarioService

class FakeUsuario:
    def __init__(self, id_usuario, username, email_usuario, rol, tokens=0):
        self.id_usuario = id_usuario
        self.username = username
        self.email_usuario = email_usuario
        self.rol = rol
        self.tokens = tokens

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(usuarios_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# ==============================================================================
# TESTS DE LAS VISTAS (HTML)
# ==============================================================================

def test_ver_perfil_exitoso(client, monkeypatch):
    """GET /perfil/<id> renderiza la plantilla si el solicitante es el dueño."""
    usuario_mock = FakeUsuario(id_usuario=1, username="victor", email_usuario="v@p.com", rol="ALUMNO")
    monkeypatch.setattr(UsuarioService, "obtener_usuario_por_id", lambda id_user: usuario_mock)
    
    @client.application.before_request
    def set_context():
        g.current_user = usuario_mock

    response = client.get('/perfil/1')
    assert response.status_code == 200


def test_ver_perfil_acceso_denegado(client, monkeypatch):
    """GET /perfil/<id> devuelve 403 si intentas ver un perfil ajeno."""
    usuario_mock = FakeUsuario(id_usuario=1, username="victor", email_usuario="v@p.com", rol="ALUMNO")
    
    @client.application.before_request
    def set_context():
        g.current_user = usuario_mock

    response = client.get('/perfil/99')
    assert response.status_code == 403

# ==============================================================================
# TESTS DE LA API JSON
# ==============================================================================


def test_api_modificar_usuario_exitoso(client, monkeypatch):
    """PUT /api/usuarios/<id> envía los parámetros de forma correcta al servicio."""
    captura = {}
    monkeypatch.setattr(UsuarioService, "actualizar_usuario", 
                        lambda dest, dat, sol: captura.update({"dest": dest, "dat": dat, "sol": sol}))

    response = client.put('/api/usuarios/5', 
                          json={"imagen_usuario": "foto.png"}, 
                          headers={'X-User-Id': '10'})
    
    assert response.status_code == 200
    assert response.get_json()['mensaje'] == 'Actualización realizada correctamente'
    assert captura["dest"] == 5
    assert captura["sol"] == "10"


