from flask import Flask
# 1. Asegúrate de tener las tres importaciones arriba
from src.modules.posts.controllers import posts
from src.modules.respuestas.controllers import respuestas
from src.modules.pruebas.controllers import pruebas

def create_app():
    app = Flask(__name__)

    # ... (aquí tus configuraciones de base de datos si tienes) ...

    # 2. Registra los tres uno detrás del otro, bien alineados a la izquierda (con 4 espacios de indentación)
    app.register_blueprint(pruebas, url_prefix='/pruebas')
    app.register_blueprint(posts)
    app.register_blueprint(respuestas)

    return app