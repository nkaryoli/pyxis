from src.repositories.respuesta_repository import RespuestaRepository

class RespuestaService:
    """Servicio de lógica de negocio para gestionar Respuestas."""

    @staticmethod
    def crear_respuesta(id_post, id_usuario, contenido, es_mejor=0, imagen=None):
        """
        Crea una nueva respuesta en un post.
        
        Args:
            id_post (int): ID del post al que responde.
            id_usuario (int): ID del usuario creador.
            contenido (str): Texto de la respuesta.
            es_mejor (int, optional): Indica si es marcada como mejor respuesta.
            imagen (str, optional): Ruta a la imagen adjunta.
            
        Returns:
            Respuesta: El objeto respuesta creado.
        """
        return RespuestaRepository.create(id_post, id_usuario, contenido, es_mejor, imagen)

    @staticmethod
    def obtener_respuestas_de_post(id_post):
        """Obtiene todas las respuestas asociadas a un post."""
        from src.extensions import should_include_deleted
        return RespuestaRepository.get_by_post_id(id_post, include_deleted=should_include_deleted())

    @staticmethod
    def obtener_respuestas_de_usuario(id_usuario):
        """Obtiene todas las respuestas publicadas por un usuario."""
        from src.extensions import should_include_deleted
        return RespuestaRepository.get_by_user_id(id_usuario, include_deleted=should_include_deleted())

    @staticmethod
    def obtener_por_id(id_respuesta):
        """Obtiene una respuesta específica por su ID."""
        return RespuestaRepository.get_by_id(id_respuesta)

    @staticmethod
    def eliminar_respuesta(id_respuesta):
        """Elimina lógicamente una respuesta."""
        return RespuestaRepository.delete(id_respuesta)

    @staticmethod
    def modificar_respuesta(id_respuesta, contenido=None, imagen=None, es_mejor=None, is_deleted=None):
        """
        Modifica los campos de una respuesta existente.
        
        Args:
            id_respuesta (int): ID de la respuesta a editar.
            contenido (str, optional): Nuevo texto de la respuesta.
            imagen (str, optional): Nueva imagen adjunta.
            es_mejor (int, optional): Nuevo estado de mejor respuesta.
            is_deleted (bool, optional): Estado de eliminación.
            
        Returns:
            Respuesta: Objeto modificado de la respuesta.
        """
        return RespuestaRepository.update(id_respuesta, contenido, imagen, es_mejor, is_deleted)
