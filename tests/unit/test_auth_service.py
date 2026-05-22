from types import SimpleNamespace
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.auth_service import AuthService

import pytest


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
    

def test_autenticar_usuario_devuelve_usuario_y_token(app, monkeypatch):
    """Comprueba que el login devuelve el usuario autenticado y un token firmado."""
    password_hash = generate_password_hash("Secreta123")
    usuario = SimpleNamespace(
        id_usuario=15,
        username="alumno",
        email_usuario="alumno@monlau.com",
        password_usuario=password_hash,
        rol="ALUMNO",
    )

    monkeypatch.setattr(
        "src.services.auth_service.UsuarioRepository.get_by_email",
        lambda email: usuario,
    )

    with app.app_context():
        resultado = AuthService.autenticar_usuario(
            {"email": "alumno@monlau.com", "password": "Secreta123"}
        )

    assert resultado["usuario"] is usuario
    assert isinstance(resultado["token"], str)
    assert resultado["token"]


def test_validar_token_rechaza_tokens_invalidos(app):
    """Comprueba que un token inválido lanza un error de validación."""
    with app.app_context():
        try:
            AuthService.validar_token("token-invalido")
        except ValueError as exc:
            assert "no es válido" in str(exc)
        else:
            raise AssertionError("Se esperaba ValueError para un token inválido")


def test_registrar_usuario_falla_si_passwords_no_coinciden(app):
    """Comprueba que el registro falla cuando las contraseñas no coinciden."""

    with app.app_context():
        with pytest.raises(ValueError, match="Las contraseñas no coinciden"):
            AuthService.registrar_usuario(
                {
                    "email": "alumno@monlau.com",
                    "password": "Secreta123",
                    "confirm_password": "OtraPassword456",
                }
            )
            

