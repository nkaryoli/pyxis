# Solo importas los modelos de su propia carpeta
from src.models.post import Post
from src.models.respuesta import Respuesta

# Opcional: puedes listarlos aquí para que al importar 'src.models' se carguen todos
__all__ = ["Post", "Respuesta"]