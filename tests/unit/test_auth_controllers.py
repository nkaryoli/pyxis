from types import SimpleNamespace

def test_login_setea_cookie_auth_token(client, monkeypatch):
    """Comprueba que el login devuelve JSON y deja la cookie auth_token."""
    usuario = SimpleNamespace(
        id_usuario=22,
        username="alumno",
        email_usuario="alumno@monlau.com",
        rol="ALUMNO",
    )

    monkeypatch.setattr(
        "src.services.auth_service.AuthService.autenticar_usuario",
        lambda datos: {"usuario": usuario, "token": "token-prueba"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "alumno@monlau.com", "password": "Secreta123"},
        headers={"Accept": "application/json"},
    )

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()["mensaje"] == "Inicio de sesión correcto"
    assert "auth_token=token-prueba" in response.headers.get("Set-Cookie", "")
    assert "HttpOnly" in response.headers.get("Set-Cookie", "")


def test_auth_me_devuelve_usuario_autenticado(client, monkeypatch):
    """Comprueba que /auth/me devuelve el usuario autenticado cuando hay cookie válida."""
    usuario = SimpleNamespace(
        id_usuario=22,
        username="alumno",
        email_usuario="alumno@monlau.com",
        rol="ALUMNO",
        tokens=120,
    )

    monkeypatch.setattr(
        "src.services.auth_service.AuthService.validar_token",
        lambda token, max_age=86400: {
            "id_usuario": 22,
            "email_usuario": "alumno@monlau.com",
            "rol": "ALUMNO",
        },
    )
    monkeypatch.setattr(
        "src.services.auth_service.UsuarioRepository.get_by_id",
        lambda id_usuario: usuario,
    )
    client.set_cookie("auth_token", "token-prueba")
    response = client.get(
		"/auth/me",
		headers={
			"Accept": "application/json",
		},
	)

    assert response.status_code == 200
    assert response.is_json
    body = response.get_json()
    assert body["id_usuario"] == 22
    assert body["username"] == "alumno"
    assert body["email_usuario"] == "alumno@monlau.com"
    assert body["rol"] == "ALUMNO"
    assert body["puntos"] == 120


def test_auth_me_sin_cookie_devuelve_401(client):
    """Comprueba que /auth/me responde 401 si no hay cookie de autenticación."""
    response = client.get("/auth/me", headers={"Accept": "application/json"})

    assert response.status_code == 401
    assert response.is_json
    assert response.get_json()["error"] == "Autenticación requerida"


def test_logout_borra_cookie(client):
    """Comprueba que logout responde OK y elimina la cookie auth_token."""
    response = client.post("/auth/logout", headers={"Accept": "application/json"})
    
    cookie = response.headers.get("Set-Cookie", "")
    
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()["mensaje"] == "Sesión cerrada correctamente"
    assert "auth_token=;" in cookie
    assert "Expires=" in cookie or "Max-Age=0" in cookie


def test_login_get_devuelve_template(client):
    """Comprueba que GET /auth/login devuelve el formulario de login."""

    response = client.get("/auth/login")

    assert response.status_code == 200
    assert b"html" in response.data.lower() or response.data


def test_login_post_html_redirige_y_setea_cookie(client, monkeypatch):
    """Comprueba que el login en modo HTML redirige y setea cookie auth_token."""

    usuario = SimpleNamespace(
        id_usuario=22,
        username="alumno",
        email_usuario="alumno@monlau.com",
        rol="ALUMNO",
    )

    monkeypatch.setattr(
        "src.services.auth_service.AuthService.autenticar_usuario",
        lambda datos: {"usuario": usuario, "token": "token-prueba"},
    )

    response = client.post(
        "/auth/login",
        data={
            "email": "alumno@monlau.com",
            "password": "Secreta123",
        },
    )

    assert response.status_code in (301, 302)

    cookie = response.headers.get("Set-Cookie", "")
    assert "auth_token=token-prueba" in cookie
    assert "HttpOnly" in cookie

    assert "/perfil" in response.headers.get("Location", "") or "usuario" in response.headers.get("Location", "")