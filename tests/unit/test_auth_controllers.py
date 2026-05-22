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

