from flask import current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from src.repositories.usuario_repository import UsuarioRepository
from functools import wraps
from flask import request, g, jsonify, redirect, url_for


class AuthService:
    """Lógica de autenticación: registro, login y tokens firmados."""

    DOMINIOS_VALIDOS = ('@monlau.com', '@campus.monlau.com', '@pixys.com')
    ROL_POR_DEFECTO = 'ALUMNO'
    SALT_TOKEN = 'pyxis-auth'

    @staticmethod
    def _normalizar_email(email):
        """Normaliza el correo para evitar diferencias por mayúsculas o espacios."""
        return (email or '').strip().lower()

    @classmethod
    def _generar_username(cls, email):
        """Genera un nombre de usuario a partir de la parte local del correo."""
        parte_local = email.split('@', 1)[0]
        return parte_local[:-6] if len(parte_local) > 6 else parte_local

    @staticmethod
    def _obtener_serializer():
        """Construye el serializador usado para firmar y validar tokens."""
        secret_key = current_app.config.get('SECRET_KEY')
        if not secret_key:
            raise RuntimeError('SECRET_KEY no configurada.')
        return URLSafeTimedSerializer(secret_key, salt=AuthService.SALT_TOKEN)

    @classmethod
    def registrar_usuario(cls, datos):
        """Valida los datos y crea un usuario nuevo con contraseña hasheada."""
        return cls.registrar_usuario_con_rol(datos, cls.ROL_POR_DEFECTO)

    @classmethod
    def registrar_usuario_con_rol(cls, datos, rol):
        """Crea un usuario permitiendo definir el rol explícitamente."""
        email = cls._normalizar_email(datos.get('email_usuario') or datos.get('email'))
        password = datos.get('password_usuario') or datos.get('password')
        confirmacion = datos.get('confirm_password_usuario') or datos.get('confirm_password')

        if not email or not password:
            raise ValueError('El email y la contraseña son obligatorios.')

        if confirmacion is not None and confirmacion != password:
            raise ValueError('Las contraseñas no coinciden.')

        if not any(email.endswith(domino) for domino in cls.DOMINIOS_VALIDOS):
            raise ValueError('El email debe pertenecer a un dominio autorizado.')

        if UsuarioRepository.get_by_email(email):
            raise ValueError('Este correo electrónico ya está registrado.')

        username = cls._generar_username(email)
        password_hash = generate_password_hash(password)
        rol_normalizado = (rol or cls.ROL_POR_DEFECTO).upper()

        return UsuarioRepository.create(username, email, password_hash, rol_normalizado)

    @classmethod
    def autenticar_usuario(cls, datos):
        """Comprueba credenciales válidas y devuelve el usuario junto al token."""
        email = cls._normalizar_email(datos.get('email_usuario') or datos.get('email'))
        password = datos.get('password_usuario') or datos.get('password')

        if not email or not password:
            raise ValueError('El email y la contraseña son obligatorios.')

        usuario = UsuarioRepository.get_by_email(email)
        if not usuario:
            raise ValueError('Credenciales inválidas.')

        if not usuario.is_active:
            raise ValueError('Esta cuenta de usuario se encuentra inactiva o ha sido desactivada.')

        if not check_password_hash(usuario.password_usuario, password):
            raise ValueError('Credenciales inválidas.')

        token = cls.generar_token(usuario)
        return {'usuario': usuario, 'token': token}

    @classmethod
    def generar_token(cls, usuario):
        """Genera un token firmado con la información básica del usuario."""
        serializer = cls._obtener_serializer()
        payload = {
            'id_usuario': usuario.id_usuario,
            'email_usuario': usuario.email_usuario,
            'rol': usuario.rol,
        }
        return serializer.dumps(payload)

    @classmethod
    def validar_token(cls, token, max_age=86400):
        """Valida un token firmado y devuelve su contenido si sigue siendo válido."""
        serializer = cls._obtener_serializer()
        try:
            return serializer.loads(token, max_age=max_age)
        except SignatureExpired as e:
            raise ValueError('El token ha expirado.') from e
        except BadSignature as e:
            raise ValueError('El token no es válido.') from e


    @classmethod
    def token_required(cls, func):
        """Decorador para proteger endpoints que requieren autenticación.

        Busca el token en la cookie `auth_token` o en el header `Authorization: Bearer ...`.
        Valida el token y, si es válido, adjunta el usuario actual en `flask.g.current_user`.
        Si falta o es inválido, redirige al login para peticiones HTML o devuelve 401 en JSON.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            wants_json = (
                request.is_json or 
                'application/json' in request.headers.get('Accept', '') or
                request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            )

            token = request.cookies.get('auth_token')

            # Fallback a header Authorization
            if not token:
                auth_header = request.headers.get('Authorization', '')
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ', 1)[1].strip()

            if not token:
                if not wants_json:
                    return redirect(url_for('auth.login'))
                return jsonify({'error': 'Autenticación requerida'}), 401

            try:
                payload = cls.validar_token(token)
            except ValueError as e:
                if not wants_json:
                    return redirect(url_for('auth.login'))
                return jsonify({'error': str(e)}), 401

            id_usuario = payload.get('id_usuario')
            if not id_usuario:
                if not wants_json:
                    return redirect(url_for('auth.login'))
                return jsonify({'error': 'Token inválido (sin id)'}), 401

            usuario = UsuarioRepository.get_by_id(id_usuario)
            if not usuario:
                if not wants_json:
                    return redirect(url_for('auth.login'))
                return jsonify({'error': 'Usuario no encontrado'}), 401

            if not usuario.is_active:
                if not wants_json:
                    return redirect(url_for('auth.login'))
                return jsonify({'error': 'Tu cuenta de usuario ha sido desactivada'}), 401

            # Attach current user to flask.g
            g.current_user = usuario
            return func(*args, **kwargs)

        return wrapper