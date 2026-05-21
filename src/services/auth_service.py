from flask import current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from src.repositories.usuario_repository import UsuarioRepository


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

        return UsuarioRepository.create(username, email, password_hash, cls.ROL_POR_DEFECTO)

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