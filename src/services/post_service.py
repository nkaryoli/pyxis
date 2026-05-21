from src.repositories.post_repository import PostRepository

class PostService:

    @staticmethod
    def listar_todos():
        return PostRepository.get_all()

    @staticmethod
    def ver_posts_por_usuario(id_usuario):
        return PostRepository.get_by_user_id(id_usuario)

    @staticmethod
    def crear_post(titulo, contenido, id_usuario):
        return PostRepository.create(titulo, contenido, id_usuario)


    @staticmethod
    def eliminar_post(id_post):
        exito = PostRepository.delete(id_post)
        if not exito:
            raise Exception("El post no existe")
        return True
    
    @staticmethod
    def obtener_por_id(id_post):
        return PostRepository.get_by_post_id(id_post)