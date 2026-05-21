from src.repositories.respuesta_repository import RespuestaRepository

class RespuestaService:

    @staticmethod
    def crear_respuesta(id_post, id_usuario, contenido, es_mejor=0, imagen=None):
        return RespuestaRepository.create(id_post, id_usuario, contenido, es_mejor, imagen)

    @staticmethod
    def obtener_respuestas_de_post(id_post):
        return RespuestaRepository.get_by_post_id(id_post)

    @staticmethod
    def obtener_respuestas_de_usuario(id_usuario):
        return RespuestaRepository.get_by_user_id(id_usuario)

    @staticmethod
    def obtener_por_id(id_respuesta):
        # Este método es el que usa el controlador para verificar quién es el dueño
        return RespuestaRepository.get_by_id(id_respuesta)

    @staticmethod
    def eliminar_respuesta(id_respuesta):
        return RespuestaRepository.delete(id_respuesta)

    @staticmethod
    def modificar_respuesta(id_respuesta, contenido=None, imagen=None):
        return RespuestaRepository.update(id_respuesta, contenido, imagen)