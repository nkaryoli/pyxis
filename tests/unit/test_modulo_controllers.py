"""
Tests unitarios para los controladores de Módulos (Rutas API).

Hacemos peticiones HTTP simuladas usando la fixture `client` y mockeamos 
los métodos de `ModuloService` para probar las respuestas HTTP puramente.
"""

import pytest
from src.services.modulo_service import ModuloService

class FakeModulo:
    def __init__(self, codigo_modulo, nombre_asignatura, curso_modulo):
        self.codigo_modulo = codigo_modulo
        self.nombre_asignatura = nombre_asignatura
        self.curso_modulo = curso_modulo

def test_get_modulos_endpoint(client, monkeypatch):
    """Prueba el endpoint GET /api/modulos/"""
    def fake_obtener_todos():
        return [FakeModulo("PROG", "Programación", "1DAM")]
    
    monkeypatch.setattr(ModuloService, "obtener_todos_los_modulos", staticmethod(fake_obtener_todos))

    response = client.get('/api/modulos/')
    
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['codigo_modulo'] == "PROG"

def test_post_modulo_endpoint_valido(client, monkeypatch):
    """Prueba el endpoint POST /api/modulos/ para creación exitosa (201)"""
    def fake_crear(codigo, nombre, curso, rol):
        return FakeModulo(codigo, nombre, curso)
    
    monkeypatch.setattr(ModuloService, "crear_nuevo_modulo", staticmethod(fake_crear))
    
    payload = {
        "codigo_modulo": "BBDD",
        "nombre_asignatura": "Bases de Datos",
        "curso_modulo": "1DAM",
        "rol_usuario_activo": "PROFESOR"
    }
    response = client.post('/api/modulos/', json=payload)
    
    assert response.status_code == 201
    assert response.json['nombre_asignatura'] == "Bases de Datos"

def test_post_modulo_endpoint_error(client, monkeypatch):
    """Prueba que el endpoint POST devuelve 400 cuando el servicio lanza error"""
    def fake_crear_error(*args):
        raise ValueError("Error de negocio simulado")
    
    monkeypatch.setattr(ModuloService, "crear_nuevo_modulo", staticmethod(fake_crear_error))
    
    response = client.post('/api/modulos/', json={})
    
    assert response.status_code == 400
    assert "Error de negocio simulado" in response.json['error']

def test_put_modulo_endpoint_valido(client, monkeypatch):
    """Prueba el endpoint PUT /api/modulos/<codigo> (200)"""
    def fake_modificar(codigo, nombre, curso, rol):
        return FakeModulo(codigo, nombre, curso)

    monkeypatch.setattr(ModuloService, "modificar_modulo", staticmethod(fake_modificar))
    
    payload = {
        "nombre_asignatura": "Nuevo Nombre",
        "curso_modulo": "2DAM",
        "rol_usuario_activo": "ADMINISTRADOR"
    }
    response = client.put('/api/modulos/PROG', json=payload)
    
    assert response.status_code == 200
    assert response.json['nombre_asignatura'] == "Nuevo Nombre"

def test_delete_modulo_endpoint_valido(client, monkeypatch):
    """Prueba el endpoint DELETE /api/modulos/<codigo> (200)"""
    def fake_eliminar(codigo, rol):
        return True

    monkeypatch.setattr(ModuloService, "eliminar_modulo_existente", staticmethod(fake_eliminar))
    
    payload = {"rol_usuario_activo": "PROFESOR"}
    response = client.delete('/api/modulos/PROG', json=payload)
    
    assert response.status_code == 200
    assert "eliminado correctamente" in response.json['message']