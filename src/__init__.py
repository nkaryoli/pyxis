from flask import Flask
from config import Config
from src.extensions import init_db

def create_app():
    app = Flask(__name__)
    app.debug = True
    # Cargamos la configuración desde config.py
    app.config.from_object(Config)
    
    # Construimos la URL de conexión a la BD
    db_url = (
        f"mysql+pymysql://{app.config['MYSQL_USER']}:"
        f"{app.config['MYSQL_PASSWORD']}@"
        f"{app.config['MYSQL_HOST']}/"
        f"{app.config['MYSQL_DB']}"
    )
    
    # Inicializamos la base de datos
    init_db(db_url)
    
    # Importamos y registramos tus Blueprints (los módulos del foro)
    #from src.modules.auth.controllers import auth
    #from src.modules.asignaturas.controllers import asignaturas
    #from src.modules.pruebas.controllers import pruebas
    from src.modules.posts.controllers import posts
    from src.modules.respuestas.controllers import respuestas

    #app.register_blueprint(auth, url_prefix='/auth')
    #app.register_blueprint(asignaturas, url_prefix='/')
    #app.register_blueprint(pruebas, url_prefix='/pruebas')
    app.register_blueprint(posts)
    app.register_blueprint(respuestas)
    
    return app