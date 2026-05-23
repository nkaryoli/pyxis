from types import SimpleNamespace
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.auth_service import AuthService

import pytest

# =========================================================
# ....................... REGISTER ........................
# =========================================================

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


def test_registrar_usuario_falla_si_email_ya_existe(app, monkeypatch):
    """Comprueba que el registro falla si el email ya está registrado."""

    usuario_existente = SimpleNamespace(
        id_usuario=1,
        email_usuario="alumno@monlau.com",
    )

    monkeypatch.setattr(
        "src.services.auth_service.UsuarioRepository.get_by_email",
        lambda email: usuario_existente,
    )

    with app.app_context():
        with pytest.raises(
            ValueError,
            match="ya está registrado",
        ):
            AuthService.registrar_usuario(
                {
                    "email": "alumno@monlau.com",
                    "password": "Secreta123",
                    "confirm_password": "Secreta123",
                }
            )


def test_registrar_usuario_rechaza_dominios_no_autorizados(app):
    """Comprueba que solo se permiten emails de dominios autorizados."""

    with app.app_context():
        with pytest.raises(
            ValueError,
            match="dominio autorizado",
        ):
            AuthService.registrar_usuario(
                {
                    "email": "usuario@gmail.com",
                    "password": "Secreta123",
                    "confirm_password": "Secreta123",
                }
            )


# =========================================================
# ........................ LOGIN ..........................
# =========================================================

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


def test_autenticar_usuario_falla_si_usuario_no_existe(app, monkeypatch):
    """Comprueba que el login falla cuando el usuario no existe."""

    monkeypatch.setattr(
        "src.services.auth_service.UsuarioRepository.get_by_email",
        lambda email: None,
    )

    with app.app_context():
        with pytest.raises(
            ValueError,
            match="Credenciales inválidas",
        ):
            AuthService.autenticar_usuario(
                {
                    "email": "inexistente@monlau.com",
                    "password": "Secreta123",
                }
            )


def test_autenticar_usuario_falla_si_password_es_incorrecta(app, monkeypatch):
    """Comprueba que el login falla si la contraseña es incorrecta."""

    password_hash = generate_password_hash("PasswordCorrecta")

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
        with pytest.raises(
            ValueError,
            match="Credenciales inválidas",
        ):
            AuthService.autenticar_usuario(
                {
                    "email": "alumno@monlau.com",
                    "password": "PasswordIncorrecta",
                }
            )


# =========================================================
# ........................ TOKENS .........................
# =========================================================

def test_validar_token_rechaza_tokens_invalidos(app):
    """Comprueba que un token inválido lanza un error de validación."""
    with app.app_context():
        try:
            AuthService.validar_token("token-invalido")
        except ValueError as exc:
            assert "no es válido" in str(exc)
        else:
            raise AssertionError("Se esperaba ValueError para un token inválido")


def test_validar_token_expira_inmediatamente(app):
    """Comprueba que un token recién generado se considera expirado si se pasa max_age negativo."""

    usuario = SimpleNamespace(id_usuario=99, email_usuario="x@monlau.com", rol="ALUMNO")

    with app.app_context():
        token = AuthService.generar_token(usuario)

        with pytest.raises(ValueError, match="ha expirado"):
            AuthService.validar_token(token, max_age=-1)


# =========================================================
# ................ DECORADOR token_required ...............
# =========================================================

def test_token_required_accepts_authorization_header(app, client, monkeypatch):
    """Comprueba que el decorador acepta el token enviado en el header Authorization: Bearer."""

    usuario = SimpleNamespace(
        id_usuario=33,
        email_usuario="otro@monlau.com",
        rol="ALUMNO",
    )

    monkeypatch.setattr(
        "src.services.auth_service.AuthService.validar_token",
        lambda token, max_age=86400: {"id_usuario": 33, "email_usuario": "otro@monlau.com", "rol": "ALUMNO"},
    )

    monkeypatch.setattr(
        "src.services.auth_service.UsuarioRepository.get_by_id",
        lambda id_usuario: usuario,
    )

    from flask import jsonify, g

    @app.route("/test-protected-header")
    @AuthService.token_required
    def protected_header():
        return jsonify({"ok": True, "user_id": g.current_user.id_usuario})

    response = client.get("/test-protected-header", headers={"Authorization": "Bearer token-prueba"})

    assert response.status_code == 200
    assert response.json["ok"] is True
    assert response.json["user_id"] == 33
