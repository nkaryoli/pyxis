from src.extensions import get_session
from src.models.respuesta import Respuesta

class RespuestaRepository:

    @staticmethod
    def get_by_post(id_post):
        session = get_session()
        try:
            return session.query(Respuesta).filter_by(id_post=id_post).all()
        finally:
            session.close()

    @staticmethod
    def get_by_user(id_usuario):
        session = get_session()
        try:
            return session.query(Respuesta).filter_by(id_usuario=id_usuario).all()
        finally:
            session.close()

    @staticmethod
    def create(id_post, id_usuario, contenido, es_mejor=0, imagen=None):
        session = get_session()
        try:
            nueva = Respuesta(
                id_post=id_post,
                id_usuario=id_usuario,
                contenido_respuesta=contenido,
                es_mejor_respuesta=es_mejor,
                imagen_respuesta=imagen
            )
            session.add(nueva)
            session.commit()
            session.refresh(nueva)
            return nueva
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    
    @staticmethod
    def delete(id_respuesta):
        session = get_session()
        try:
            respuesta = session.query(Respuesta).filter_by(id_respuesta=id_respuesta).first()
            if not respuesta:
                return False
            session.delete(respuesta)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()