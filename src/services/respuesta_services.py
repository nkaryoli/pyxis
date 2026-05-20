from src.repositories.respuesta_repository import RespuestaRepository

class RespuestaService:

    @staticmethod
    def obtener_respuestas_de_post(id_post):
        """Recupera todas las respuestas asociadas a un post."""
        if not id_post:
            raise ValueError("Se requiere un id_post válido")
        return RespuestaRepository.get_by_post(id_post)

    @staticmethod
    def obtener_respuestas_de_usuario(id_usuario):
        """Recupera todas las respuestas redactadas por un usuario específico."""
        if not id_usuario:
            raise ValueError("Se requiere un id_usuario válido")
        return RespuestaRepository.get_by_user(id_usuario)

    @staticmethod
    def crear_respuesta(id_post, id_usuario, contenido, es_mejor=0, imagen=None):
        """Aplica validaciones de negocio antes de mandar a guardar la respuesta."""
        # Validación: Evitamos que guarden texto vacío o puros espacios
        if not contenido or contenido.strip() == "":
            raise ValueError("El contenido de la respuesta no puede estar vacío")
            
        # Pasamos los datos limpios al repositorio
        return RespuestaRepository.create(
            id_post=id_post,
            id_usuario=id_usuario,
            contenido=contenido,
            es_mejor=es_mejor,
            imagen=imagen
        )