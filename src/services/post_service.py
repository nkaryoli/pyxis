from src.repositories.post_repository import PostRepository
from src.services.modulo_service import ModuloService

class PostService:

    @staticmethod
    def listar_todos():
        from src.extensions import should_include_deleted
        return PostRepository.get_all(include_deleted=should_include_deleted())

    @staticmethod
    def ver_posts_por_usuario(id_usuario):
        from src.extensions import should_include_deleted
        return PostRepository.get_by_user_id(id_usuario, include_deleted=should_include_deleted())

    @staticmethod
    def crear_post(titulo, contenido, id_usuario, codigo_modulo, imagen=None):
        return PostRepository.create(titulo, contenido, id_usuario, codigo_modulo, imagen)

    @staticmethod
    def eliminar_post(id_post):
        exito = PostRepository.delete(id_post)
        if not exito:
            raise Exception("El post no existe")
        return True
    
    @staticmethod
    def obtener_por_id(id_post):
        return PostRepository.get_by_id(id_post)
    
    @staticmethod
    def modificar_post(id_post, titulo=None, contenido=None, codigo_modulo=None, imagen=None, fecha_creacion=None):
        return PostRepository.update(id_post, titulo, contenido, codigo_modulo, imagen, fecha_creacion)
    
    
    @staticmethod
    def ver_posts_por_modulo(codigo_modulo):
        from src.extensions import should_include_deleted
        return PostRepository.get_by_modulo_code(codigo_modulo, include_deleted=should_include_deleted())
    
    @staticmethod
    def listar_recientes():
        from src.extensions import should_include_deleted
        return PostRepository.get_recent(include_deleted=should_include_deleted())
    
    @staticmethod
    def obtener_todos_los_modulos():
        lista_modulos = ModuloService.obtener_todos_los_modulos()
        return lista_modulos
    

    @staticmethod
    def buscar_por_relevancia(query):
        todos_los_posts = PostService.listar_todos()
        query_lowercase = query.lower()
        
        coinciden_en_titulo = []
        coinciden_en_contenido = []
        
        for post in todos_los_posts:
            titulo = (post.titulo_post or "").lower()
            contenido = (post.contenido_post or "").lower()
            
            if query_lowercase in titulo:
                coinciden_en_titulo.append(post)
            elif query_lowercase in contenido:
                coinciden_en_contenido.append(post)
                
        return coinciden_en_titulo + coinciden_en_contenido



