from types import SimpleNamespace
import pytest
from src.services.respuesta_service import RespuestaService

# Helper para generar respuestas simuladas con la estructura del Repositorio
def crear_mock_respuesta(id_respuesta=1, id_post=5, id_usuario=10, contenido="Respuesta de prueba"):
    return SimpleNamespace(
        id_respuesta=id_respuesta,
        id_post=id_post,
        id_usuario=id_usuario,
        contenido=contenido,
        es_mejor=0,
        imagen=None
    )



def test_crear_respuesta_service(monkeypatch):
    """Comprueba que el servicio delega correctamente al repositorio para crear una respuesta."""
    mock_creada = crear_mock_respuesta(id_respuesta=10, contenido="Solución exacta")

    # Interceptamos RespuestaRepository.create
    monkeypatch.setattr(
        "src.services.respuesta_service.RespuestaRepository.create",
        lambda id_post, id_usuario, contenido, es_mejor, imagen: mock_creada
    )

    resultado = RespuestaService.crear_respuesta(
        id_post=5,
        id_usuario=10,
        contenido="Solución exacta"
    )

    assert resultado.id_respuesta == 10
    assert resultado.contenido == "Solución exacta"


def test_obtener_respuestas_de_post_service(monkeypatch):
    """Comprueba que el servicio obtiene la lista de respuestas asociadas a un post."""
    mock_lista = [crear_mock_respuesta(id_respuesta=1, id_post=5), crear_mock_respuesta(id_respuesta=2, id_post=5)]

    monkeypatch.setattr(
        "src.services.respuesta_service.RespuestaRepository.get_by_post_id",
        lambda id_post: mock_lista if id_post == 5 else []
    )

    resultado = RespuestaService.obtener_respuestas_de_post(5)

    assert len(resultado) == 2
    assert resultado[0].id_post == 5
    assert resultado[1].id_post == 5




def test_obtener_respuestas_de_usuario_service(monkeypatch):
    """Comprueba que el servicio filtra las respuestas pertenecientes a un usuario."""
    mock_lista = [crear_mock_respuesta(id_respuesta=1, id_usuario=44)]

    monkeypatch.setattr(
        "src.services.respuesta_service.RespuestaRepository.get_by_user_id",
        lambda id_usuario: mock_lista if id_usuario == 44 else []
    )

    resultado = RespuestaService.obtener_respuestas_de_usuario(44)

    assert len(resultado) == 1
    assert resultado[0].id_usuario == 44




def test_obtener_por_id_service(monkeypatch):
    """Comprueba que el servicio recupera la respuesta exacta usando su ID."""
    mock_resp = crear_mock_respuesta(id_respuesta=12)

    monkeypatch.setattr(
        "src.services.respuesta_service.RespuestaRepository.get_by_id",
        lambda id_respuesta: mock_resp if id_respuesta == 12 else None
    )

    resultado = RespuestaService.obtener_por_id(12)

    assert resultado is not None
    assert resultado.id_respuesta == 12



def test_eliminar_respuesta_service(monkeypatch):
    """Comprueba que el servicio retorna el resultado de la eliminación del repositorio (True/False)."""
    monkeypatch.setattr(
        "src.services.respuesta_service.RespuestaRepository.delete",
        lambda id_respuesta: True
    )

    resultado = RespuestaService.eliminar_respuesta(1)
    assert resultado is True


def test_modificar_respuesta_service(monkeypatch):
    """Comprueba que el servicio actualiza los campos de la respuesta correctamente."""
    mock_actualizada = crear_mock_respuesta(id_respuesta=1, contenido="Contenido Modificado")

    monkeypatch.setattr(
        "src.services.respuesta_service.RespuestaRepository.update",
        lambda id_respuesta, contenido, imagen: mock_actualizada
    )

    resultado = RespuestaService.modificar_respuesta(id_respuesta=1, contenido="Contenido Modificado")

    assert resultado.id_respuesta == 1
    assert resultado.contenido == "Contenido Modificado"