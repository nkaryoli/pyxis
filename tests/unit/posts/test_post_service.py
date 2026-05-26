from types import SimpleNamespace
import pytest
from src.services.post_service import PostService


def crear_mock_post(id_post=1, titulo="Test", id_usuario=10):
    return SimpleNamespace(
        id_post=id_post,
        titulo=titulo,
        contenido="Contenido de prueba",
        id_usuario=id_usuario,
        codigo_modulo="M06",
        imagen=None
    )


def test_listar_todos_service(monkeypatch):
    """Comprueba que el servicio retorna la lista de posts del repositorio."""
    mock_lista = [crear_mock_post(1), crear_mock_post(2)]
    
    # Interceptamos PostRepository.get_all
    monkeypatch.setattr(
        "src.services.post_service.PostRepository.get_all",
        lambda: mock_lista
    )
    
    resultado = PostService.listar_todos()
    
    assert len(resultado) == 2
    assert resultado[0].id_post == 1
    assert resultado[1].id_post == 2



def test_ver_posts_por_usuario_service(monkeypatch):
    """Comprueba que filtra correctamente los posts por ID de usuario."""
    mock_lista = [crear_mock_post(id_post=1, id_usuario=10)]
    
    monkeypatch.setattr(
        "src.services.post_service.PostRepository.get_by_user_id",
        lambda id_user: mock_lista if id_user == 10 else []
    )
    
    resultado = PostService.ver_posts_por_usuario(10)
    
    assert len(resultado) == 1
    assert resultado[0].id_usuario == 10



def test_crear_post_service(monkeypatch):
    """Comprueba que el servicio pasa los parámetros correctos para crear un post."""
    post_creado = crear_mock_post(id_post=5, titulo="Nuevo", id_usuario=22)
    
    monkeypatch.setattr(
        "src.services.post_service.PostRepository.create",
        lambda titulo, contenido, id_usuario, codigo_modulo, imagen: post_creado
    )
    
    resultado = PostService.crear_post(
        titulo="Nuevo", 
        contenido="Contenido", 
        id_usuario=22, 
        codigo_modulo="M06"
    )
    
    assert resultado.id_post == 5
    assert resultado.titulo == "Nuevo"



def test_eliminar_post_exito(monkeypatch):
    """Comprueba que el servicio retorna True si el repositorio borra con éxito."""
    monkeypatch.setattr(
        "src.services.post_service.PostRepository.delete",
        lambda id_post: True
    )
    
    resultado = PostService.eliminar_post(1)
    assert resultado is True


def test_eliminar_post_no_existe_lanza_excepcion(monkeypatch):
    """Comprueba que si el repositorio devuelve False, el servicio lanza un Exception."""
    monkeypatch.setattr(
        "src.services.post_service.PostRepository.delete",
        lambda id_post: False
    )
    
    with pytest.raises(Exception) as exc_info:
        PostService.eliminar_post(999)
        
    assert str(exc_info.value) == "El post no existe"



def test_obtener_por_id_service(monkeypatch):
    """Comprueba que el servicio obtiene el post correcto por su ID."""
    mock_post = crear_mock_post(id_post=42)
    
    monkeypatch.setattr(
        "src.services.post_service.PostRepository.get_by_id",
        lambda id_post: mock_post if id_post == 42 else None
    )
    
    resultado = PostService.obtener_por_id(42)
    assert resultado.id_post == 42



def test_modificar_post_service(monkeypatch):
    """Comprueba que el servicio actualiza el post mediante el repositorio."""
    post_editado = crear_mock_post(id_post=1, titulo="Titulo Modificado")
    
    monkeypatch.setattr(
        "src.services.post_service.PostRepository.update",
        lambda id_post, titulo, contenido, codigo_modulo, imagen: post_editado
    )
    
    resultado = PostService.modificar_post(id_post=1, titulo="Titulo Modificado")
    assert resultado.titulo == "Titulo Modificado"