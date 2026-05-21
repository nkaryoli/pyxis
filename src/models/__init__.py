
from src.models.post import Post
from src.models.respuesta import Respuesta
from flask import Flask
from src.extensions import init_db  # (O las extensiones que tengas instaladas)

def create_app():
    app = Flask(__name__)
    
    # ... Aquí van tus configuraciones (Base de datos, JWT, etc.) ...
    # Ej: init_db(app)

    # 1. Importamos SOLO los módulos reales dentro de la función
    from src.modules.posts.controllers import posts
    from src.modules.respuestas.controllers import respuestas

    # 2. Registramos los blueprints que sí vas a usar
    app.register_blueprint(posts)
    app.register_blueprint(respuestas)

    return app