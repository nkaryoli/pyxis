from src.repositories.post_repository import PostRepository
from src.services.modulo_service import ModuloService

class PostService:
    """Servicio de lógica de negocio para la gestión de Posts."""

    @staticmethod
    def listar_todos():
        """Devuelve todos los posts en el sistema."""
        from src.extensions import should_include_deleted
        return PostRepository.get_all(include_deleted=should_include_deleted())

    @staticmethod
    def ver_posts_por_usuario(id_usuario):
        """Obtiene los posts creados por un usuario específico."""
        from src.extensions import should_include_deleted
        return PostRepository.get_by_user_id(id_usuario, include_deleted=should_include_deleted())

    @staticmethod
    def crear_post(titulo, contenido, id_usuario, codigo_modulo, imagen=None):
        """
        Crea un nuevo post en un módulo.
        
        Args:
            titulo (str): Título del post.
            contenido (str): Contenido del post.
            id_usuario (int): ID del creador.
            codigo_modulo (str): Código del módulo.
            imagen (str, optional): Ruta de imagen asociada.
            
        Returns:
            Post: El post creado.
        """
        return PostRepository.create(titulo, contenido, id_usuario, codigo_modulo, imagen)

    @staticmethod
    def eliminar_post(id_post):
        """Elimina un post del sistema por su ID."""
        exito = PostRepository.delete(id_post)
        if not exito:
            raise Exception("El post no existe")
        return True
    
    @staticmethod
    def obtener_por_id(id_post):
        """Obtiene el detalle de un post específico."""
        return PostRepository.get_by_id(id_post)
    
    @staticmethod
    def modificar_post(id_post, titulo=None, contenido=None, codigo_modulo=None, imagen=None, fecha_creacion=None, is_deleted=None):
        """
        Modifica los campos permitidos de un post existente.
        
        Args:
            id_post (int): ID del post.
            titulo (str, optional): Nuevo título.
            contenido (str, optional): Nuevo contenido.
            codigo_modulo (str, optional): Nuevo código de módulo.
            imagen (str, optional): Nueva imagen.
            fecha_creacion (datetime, optional): Modificación de fecha.
            is_deleted (bool, optional): Estado de borrado.
            
        Returns:
            Post: El post actualizado.
        """
        return PostRepository.update(id_post, titulo, contenido, codigo_modulo, imagen, fecha_creacion, is_deleted)
    
    @staticmethod
    def ver_posts_por_modulo(codigo_modulo):
        """Obtiene todos los posts de un módulo concreto."""
        from src.extensions import should_include_deleted
        return PostRepository.get_by_modulo_code(codigo_modulo, include_deleted=should_include_deleted())
    
    @staticmethod
    def listar_recientes():
        """Devuelve los posts creados más recientemente."""
        from src.extensions import should_include_deleted
        return PostRepository.get_recent(include_deleted=should_include_deleted())
    
    @staticmethod
    def obtener_todos_los_modulos():
        """Devuelve todos los módulos académicos disponibles."""
        lista_modulos = ModuloService.obtener_todos_los_modulos()
        return lista_modulos

    @staticmethod
    def buscar_por_relevancia(query):
        """
        Realiza una búsqueda de posts cuyo título o contenido coincida con la consulta.
        
        Args:
            query (str): Término de búsqueda.
            
        Returns:
            list[Post]: Lista de posts coincidentes ordenados por coincidencia en título y luego en contenido.
        """
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
