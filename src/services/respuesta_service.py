from src.repositories.respuesta_repository import RespuestaRepository

class RespuestaService:

    @staticmethod
    def obtener_respuestas_de_post(id_post):
        if not id_post:
            raise ValueError("Se requiere un id_post válido")
        return RespuestaRepository.get_by_post(id_post)

    @staticmethod
    def obtener_respuestas_de_usuario(id_usuario):
        if not id_usuario:
            raise ValueError("Se requiere un id_usuario válido")
        return RespuestaRepository.get_by_user(id_usuario)

    @staticmethod
    def crear_respuesta(id_post, id_usuario, contenido, es_mejor=0, imagen=None):
        if not contenido or contenido.strip() == "":
            raise ValueError("El contenido de la respuesta no puede estar vacío")
            
        return RespuestaRepository.create(
            id_post=id_post,
            id_usuario=id_usuario,
            contenido=contenido,
            es_mejor=es_mejor,
            imagen=imagen
        )


    @staticmethod
    def eliminar_respuesta(id_respuesta):
        return RespuestaRepository.delete(id_respuesta)