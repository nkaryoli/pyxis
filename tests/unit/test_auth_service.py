from types import SimpleNamespace
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.auth_service import AuthService

def test_registrar_usuario_hashea_password_y_usa_rol_por_defecto(app, monkeypatch):
    """Comprueba que el registro hashea la contraseña y aplica el rol por defecto."""
    captured = {}

    monkeypatch.setattr(
        "src.services.auth_service.UsuarioRepository.get_by_email",
        lambda email: None,
    )

    def fake_create(username, email, password_hash, rol):
        captured["username"] = username
        captured["email"] = email
        captured["password_hash"] = password_hash
        captured["rol"] = rol
        return SimpleNamespace(
            id_usuario=7,
            username=username,
            email_usuario=email,
            password_usuario=password_hash,
            rol=rol,
        )

    monkeypatch.setattr(
        "src.services.auth_service.UsuarioRepository.create",
        fake_create,
    )

    with app.app_context():
        usuario = AuthService.registrar_usuario(
            {
                "email": "alumno123@monlau.com",
                "password": "Secreta123",
                "confirm_password": "Secreta123",
            }
        )

    assert usuario.email_usuario == "alumno123@monlau.com"
    assert usuario.rol == AuthService.ROL_POR_DEFECTO
    assert captured["email"] == "alumno123@monlau.com"
    assert captured["rol"] == AuthService.ROL_POR_DEFECTO
    assert captured["password_hash"] != "Secreta123"
    assert check_password_hash(captured["password_hash"], "Secreta123")
    