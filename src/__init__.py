from flask import Flask, render_template
from config import Config
from src.extensions import init_db
import os

from src.services.modulo_service import ModuloService

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
    
    # Construimos la URL de conexión a la BD
    db_url = (
        f"mysql+pymysql://{app.config['MYSQL_USER']}:"
        f"{app.config['MYSQL_PASSWORD']}@"
        f"{app.config['MYSQL_HOST']}/"
        f"{app.config['MYSQL_DB']}"
    )
    
    # Inicializamos la base de datos
    init_db(db_url)
        
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
    
    return app