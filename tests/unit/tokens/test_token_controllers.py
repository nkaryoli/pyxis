import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from src.modules.tokens.controllers import tokens 

@pytest.fixture
def app():
    """Configura una instancia de Flask para las pruebas."""
    app = Flask(__name__)
    app.register_blueprint(tokens)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Proporciona el cliente de pruebas de Flask."""
    return app.test_client()


@patch('src.services.tokens_service.TokensService.registrar_tokens')
def test_crear_registro_exito(mock_registrar, client):
    # Simulamos el objeto que devuelve el servicio y su método to_dict()
    mock_registro = MagicMock()
    mock_registro.to_dict.return_value = {
        "id": 1, "tokens": 10, "motivo": "Buen trabajo", "trimestre": "Q1", "id_usuario": 42
    }
    mock_registrar.return_value = mock_registro

    payload = {"tokens": 10, "motivo": "Buen trabajo", "trimestre": "Q1", "id_usuario": 42}
    response = client.post('/api/tokens', json=payload)

    assert response.status_code == 201
    assert response.get_json()["mensaje"] == "Tokens registrados con éxito"
    assert response.get_json()["registro"]["id"] == 1

def test_crear_registro_faltan_campos(client):
    payload = {"tokens": 10} # Faltan campos obligatorios
    response = client.post('/api/tokens', json=payload)

    assert response.status_code == 400
    assert "Faltan campos requeridos" in response.get_json()["error"]

@patch('src.services.tokens_service.TokensService.obtener_historial_usuario')
def test_ver_historial_usuario_exito(mock_historial, client):
    mock_item = MagicMock()
    mock_item.to_dict.return_value = {"id": 1, "tokens": 5}
    mock_historial.return_value = [mock_item]

    response = client.get('/api/usuarios/42/tokens')

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["tokens"] == 5



def test_eliminar_tokens_sin_autenticacion(client):
    response = client.delete('/api/tokens/1') # Sin headers
    assert response.status_code == 401
    assert "Falta X-User-Role" in response.get_json()["error"]

def test_eliminar_tokens_permisos_insuficientes(client):
    headers = {'X-User-Role': 'ALUMNO'}
    response = client.delete('/api/tokens/1', headers=headers)
    assert response.status_code == 403
    assert "No tienes permisos" in response.get_json()["error"]

@patch('src.services.tokens_service.TokensService.eliminar_registro_tokens')
def test_eliminar_tokens_no_encontrado(mock_eliminar, client):
    mock_eliminar.return_value = False # Simula que no existía el ID
    headers = {'X-User-Role': 'PROFESOR'}
    
    response = client.delete('/api/tokens/999', headers=headers)
    
    assert response.status_code == 404
    assert "No se encontró ningún registro" in response.get_json()["error"]

@patch('src.services.tokens_service.TokensService.eliminar_registro_tokens')
def test_eliminar_tokens_exito(mock_eliminar, client):
    mock_eliminar.return_value = True
    headers = {'X-User-Role': 'ADMINISTRADOR'}

    response = client.delete('/api/tokens/1', headers=headers)

    assert response.status_code == 200
    assert "eliminado correctamente" in response.get_json()["mensaje"]




def test_ver_todos_los_tokens_alumno_denegado(client):
    headers = {'X-User-Role': 'ALUMNO'}
    response = client.get('/api/tokens', headers=headers)
    assert response.status_code == 403

@patch('src.services.tokens_service.TokensService.obtener_todos_los_tokens')
def test_ver_todos_los_tokens_profesor_exito(mock_todos, client):
    mock_item = MagicMock()
    mock_item.to_dict.return_value = {"id": 1, "tokens": 20}
    mock_todos.return_value = [mock_item]
    
    headers = {'X-User-Role': 'PROFESOR'}
    response = client.get('/api/tokens', headers=headers)

    assert response.status_code == 200
    assert len(response.get_json()) == 1



@patch('src.services.tokens_service.TokensService.obtener_todos_los_tokens')
def test_error_interno_servidor_500(mock_todos, client):
    # Forzamos una excepción genérica en el servicio para activar el bloque 'except'
    mock_todos.side_effect = Exception("Error inesperado en la base de datos")
    
    headers = {'X-User-Role': 'ADMINISTRADOR'}
    response = client.get('/api/tokens', headers=headers)

    assert response.status_code == 500
    assert response.get_json()["error"] == "Error inesperado en la base de datos"