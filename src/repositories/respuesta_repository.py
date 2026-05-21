from src.extensions import get_session
from src.models.respuesta import Respuesta

class RespuestaRepository:

    @staticmethod
    def create(id_post, id_usuario, contenido, es_mejor=0, imagen=None):
        session = get_session()
        try:
            nueva_respuesta = Respuesta(
                id_post=id_post,
                id_usuario=id_usuario,
                contenido_respuesta=contenido,
                es_mejor_respuesta=es_mejor,
                imagen_respuesta=imagen
            )
            session.add(nueva_respuesta)
            session.commit()
            session.refresh(nueva_respuesta)
            session.expunge(nueva_respuesta) # Libera el objeto para usarlo en el controlador
            return nueva_respuesta
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_post_id(id_post):
        session = get_session()
        try:
            respuestas = session.query(Respuesta).filter_by(id_post=id_post).all()
            session.expunge_all()
            return respuestas
        finally:
            session.close()

    @staticmethod
    def get_by_user_id(id_usuario):
        session = get_session()
        try:
            respuestas = session.query(Respuesta).filter_by(id_usuario=id_usuario).all()
            session.expunge_all()
            return respuestas
        finally:
            session.close()

    @staticmethod
    def get_by_id(id_respuesta):
        session = get_session()
        try:
            respuesta = session.query(Respuesta).filter_by(id_respuesta=id_respuesta).first()
            if respuesta:
                session.expunge(respuesta)
            return respuesta
        finally:
            session.close()

    @staticmethod
    def delete(id_respuesta):
        session = get_session()
        try:
            respuesta = session.query(Respuesta).filter_by(id_respuesta=id_respuesta).first()
            if respuesta:
                session.delete(respuesta)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update(id_respuesta, contenido=None, imagen=None):
        session = get_session()
        try:
            respuesta = session.query(Respuesta).filter_by(id_respuesta=id_respuesta).first()
            if not respuesta:
                return None

            # Actualizamos solo si el usuario envía datos nuevos en el JSON
            if contenido is not None:
                respuesta.contenido_respuesta = contenido
            if imagen is not None:
                respuesta.imagen_respuesta = imagen # Ajusta a tu columna exacta del modelo si varía

            session.commit()
            session.refresh(respuesta)
            session.expunge(respuesta)
            return respuesta
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()