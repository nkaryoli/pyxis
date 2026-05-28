import pytest
from src.services.usuario_service import UsuarioService
from src.repositories.usuario_repository import UsuarioRepository

class FakeUsuario:
    def __init__(self, id_usuario, username, email_usuario, rol, imagen_usuario=None, tokens=0):
        self.id_usuario = id_usuario
        self.username = username
        self.email_usuario = email_usuario
        self.rol = rol
        self.imagen_usuario = imagen_usuario
        self.tokens = tokens

# ==============================================================================
# TESTS: OBTENER USUARIOS Y PUNTOS
# ==============================================================================

def test_obtener_usuario_por_id_no_existente(monkeypatch):
    """Debe lanzar ValueError si el repositorio no encuentra al usuario."""
    monkeypatch.setattr(UsuarioRepository, "get_by_id", lambda id_user: None)

    with pytest.raises(ValueError) as exc_info:
        UsuarioService.obtener_usuario_por_id(999)
    assert "El usuario con ID 999 no existe." in str(exc_info.value)


def test_obtener_puntos_usuario_exitoso(monkeypatch):
    """Debe extraer correctamente los tokens del usuario encontrado."""
    usuario_fake = FakeUsuario(id_usuario=1, username="v", email_usuario="v@p.com", rol="ALUMNO", tokens=150)
    # Evitar llamadas a la capa de posts/BD: mockeamos la función del servicio
    monkeypatch.setattr(UsuarioService, "obtener_usuario_por_id", lambda id_user: usuario_fake)

    puntos = UsuarioService.obtener_puntos_usuario(1)
    assert puntos == 150

# ==============================================================================
# TESTS: ACTUALIZAR USUARIO
# ==============================================================================

def test_actualizar_usuario_alumno_cambia_su_propia_foto(monkeypatch):
    """ALUMNO modifica su propia foto correctamente."""
    alumno_fake = FakeUsuario(id_usuario=10, username="v", email_usuario="v@p.com", rol="ALUMNO")
    # Mockeamos la resolución de solicitante/destino para evitar dependencias de BD
    monkeypatch.setattr(UsuarioService, "obtener_usuario_por_id", lambda id_user: alumno_fake)
    
    datos_recibidos = {}
    monkeypatch.setattr(UsuarioRepository, "update", lambda id_dest, d: datos_recibidos.update(d) or alumno_fake)

    datos_nuevos = {"imagen_usuario": "nueva.png", "rol": "ADMINISTRADOR"}
    UsuarioService.actualizar_usuario(10, datos_nuevos, 10)

    assert "imagen_usuario" in datos_recibidos
    assert "rol" not in datos_recibidos


def test_actualizar_usuario_alumno_intenta_editar_otro_usuario(monkeypatch):
    """ALUMNO lanza ValueError al intentar editar un ID ajeno."""
    alumno_solicitante = FakeUsuario(id_usuario=10, username="a1", email_usuario="a1@p.com", rol="ALUMNO")
    usuario_destino = FakeUsuario(id_usuario=99, username="a2", email_usuario="a2@p.com", rol="ALUMNO")

    # Mockeamos obtener_usuario_por_id para devolver objetos según id
    monkeypatch.setattr(UsuarioService, "obtener_usuario_por_id", lambda id_user: alumno_solicitante if int(id_user) == 10 else usuario_destino)

    with pytest.raises(ValueError) as exc_info:
        UsuarioService.actualizar_usuario(99, {"imagen_usuario": "h.png"}, 10)
    assert "Un alumno no puede editar los datos de otros usuarios." in str(exc_info.value)


def test_actualizar_usuario_profesor_cambia_email_duplicado(monkeypatch):
    """Lanza ValueError si un rol superior intenta cambiar a un email que ya está en uso."""
    profesor = FakeUsuario(id_usuario=2, username="p", email_usuario="p@p.com", rol="PROFESOR")
    alumno = FakeUsuario(id_usuario=10, username="a", email_usuario="a@p.com", rol="ALUMNO")

    monkeypatch.setattr(UsuarioService, "obtener_usuario_por_id", lambda id_user: profesor if int(id_user) == 2 else alumno)
    # Simular que el repositorio encuentra que el correo nuevo ya pertenece a otro
    monkeypatch.setattr(UsuarioRepository, "get_by_email", lambda email: True)

    with pytest.raises(ValueError) as exc_info:
        UsuarioService.actualizar_usuario(10, {"email_usuario": "duplicado@p.com"}, 2)
    assert "El nuevo email ya está en uso por otro usuario." in str(exc_info.value)


def test_actualizar_usuario_sin_datos_validos(monkeypatch):
    """Lanza ValueError si solo se envían campos prohibidos para actualizar."""
    profesor = FakeUsuario(id_usuario=2, username="p", email_usuario="p@p.com", rol="PROFESOR")
    alumno = FakeUsuario(id_usuario=10, username="a", email_usuario="a@p.com", rol="ALUMNO")

    monkeypatch.setattr(UsuarioService, "obtener_usuario_por_id", lambda id_user: profesor if int(id_user) == 2 else alumno)

    with pytest.raises(ValueError) as exc_info:
        UsuarioService.actualizar_usuario(10, {"id_usuario": 4, "fecha_alta": "2030-01-01"}, 2)
    assert "No se han proporcionado datos válidos para actualizar." in str(exc_info.value)

# ==============================================================================
# TESTS: ELIMINAR USUARIO
# ==============================================================================

def test_eliminar_usuario_no_autorizado():
    """Lanza ValueError si el rol no es ADMINISTRADOR."""
    with pytest.raises(ValueError) as exc_info:
        UsuarioService.eliminar_usuario(10, "PROFESOR")
    assert "No se puede eliminar a un usuario si no eres administrador." in str(exc_info.value)


def test_eliminar_usuario_exitoso(monkeypatch):
    """Permite la eliminación si el rol es ADMINISTRADOR."""
    eliminado = []
    monkeypatch.setattr(UsuarioRepository, "delete", lambda id_user: eliminado.append(id_user) or True)

    res = UsuarioService.eliminar_usuario(10, "ADMINISTRADOR")
    assert res is True
    assert 10 in eliminado