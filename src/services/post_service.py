from src.repositories.post_repository import PostRepository
from src.services.modulo_service import ModuloService

class PostService:

    @staticmethod
    def listar_todos():
        return PostRepository.get_all()

    @staticmethod
    def ver_posts_por_usuario(id_usuario):
        return PostRepository.get_by_user_id(id_usuario)

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
        return PostRepository.get_by_modulo_code(codigo_modulo)
    
    @staticmethod
    def listar_recientes():
        return PostRepository.get_recent()
    
    @staticmethod
    def obtener_todos_los_modulos():
        lista_modulos = ModuloService.obtener_todos_los_modulos()
        return lista_modulos
    


