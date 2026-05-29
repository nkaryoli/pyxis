from flask import Flask, render_template, g, request
from config import Config
from src.extensions import init_db
import os

from src.services.modulo_service import ModuloService
from src.services.auth_service import AuthService
from src.repositories.usuario_repository import UsuarioRepository


def _cargar_usuario_actual():
    """Carga el usuario autenticado en `g.current_user` si existe un token válido."""
    if getattr(g, 'current_user', None):
        return g.current_user

    token = request.cookies.get('auth_token')
    if not token:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()

    if not token:
        return None

    try:
        payload = AuthService.validar_token(token)
        id_usuario = payload.get('id_usuario')
        if not id_usuario:
            return None

        usuario = UsuarioRepository.get_by_id(id_usuario)
        if usuario:
            g.current_user = usuario
        return usuario
    except ValueError:
        return None

def create_app():
    app = Flask(__name__)

    # Cargamos la configuración desde config.py
    app.config.from_object(Config)
    # Ajustes de seguridad según entorno: activar Secure para cookies en producción
    is_prod = os.getenv('FLASK_ENV') == 'production' or os.getenv('ENV') == 'production'
    app.config['SESSION_COOKIE_SECURE'] = is_prod
    app.config['REMEMBER_COOKIE_SECURE'] = is_prod
    # Asegurar SameSite y HttpOnly por defecto para sesiones
    app.config.setdefault('SESSION_COOKIE_SAMESITE', 'Lax')
    app.config.setdefault('SESSION_COOKIE_HTTPONLY', True)

    @app.before_request
    def cargar_usuario_actual_request():
        _cargar_usuario_actual()
    
    # Construimos la URL de conexión a la BD
    db_url = (
        f"mysql+pymysql://{app.config['MYSQL_USER']}:"
        f"{app.config['MYSQL_PASSWORD']}@"
        f"{app.config['MYSQL_HOST']}/"
        f"{app.config['MYSQL_DB']}"
    )
    
    # Inicializamos la base de datos
    init_db(db_url)

    @app.context_processor
    def inyectar_usuario_actual():
        current_user = _cargar_usuario_actual()
        return {
            'current_user': current_user,
            'is_authenticated': current_user is not None,
        }
        
    @app.route('/')
    def home():
        """Renderiza la página principal con contenido simulado del foro."""
        modulos = ModuloService.obtener_todos_los_modulos()
        return render_template('home.html', modulos=modulos)
    
    # Importamos y registramos tus Blueprints (los módulos del foro)
    from src.modules.posts.controllers import posts
    from src.modules.respuestas.controllers import respuestas
    from src.modules.tokens.controllers import tokens
    from src.modules.auth.controllers import auth
    from src.modules.modulos.controllers import modulos
    from src.modules.usuario.controllers import usuarios_bp


    app.register_blueprint(posts)
    app.register_blueprint(respuestas)
    app.register_blueprint(tokens)
    app.register_blueprint(auth)
    app.register_blueprint(modulos)
    app.register_blueprint(usuarios_bp)

    # Manejadores de error global
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('errors/400.html'), 400
   
    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.html'), 401
   
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
   
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html', mensaje='Página no encontrada'), 404
   
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    return app