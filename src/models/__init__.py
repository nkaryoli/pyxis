# Importa tu blueprint desde donde esté guardado el archivo del controlador
from src.controllers.post_controller import posts

# Registra el blueprint en la aplicación
app.register_blueprint(posts)