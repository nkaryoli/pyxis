from src.extensions import get_session
from src.models.respuesta import Respuesta

class RespuestaRepository:
    """Repositorio para operaciones CRUD de la entidad Respuesta en la base de datos."""

    @staticmethod
    def create(id_post, id_usuario, contenido, es_mejor=0, imagen=None):
        """
        Crea una nueva respuesta para un post especifico.
        
        Args:
            id_post (int): ID del post al que pertenece.
            id_usuario (int): ID del usuario que responde.
            contenido (str): Texto de la respuesta.
            es_mejor (int, optional): Indica si es la mejor respuesta. Defaults to 0.
            imagen (str, optional): Ruta o nombre de la imagen adjunta. Defaults to None.
            
        Returns:
            Respuesta: Objeto de la respuesta creada.
            
        Note:
            Se utiliza session.expunge() al final para liberar el objeto de la sesión y así poder usarlo libremente en el controlador sin errores de sesión cerrada.
        """
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
            session.expunge(nueva_respuesta)
            return nueva_respuesta
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_post_id(id_post, include_deleted=False):
        """Devuelve todas las respuestas asociadas a un post."""
        session = get_session()
        try:
            query = session.query(Respuesta).filter(Respuesta.id_post == id_post)
            if not include_deleted:
                query = query.filter(Respuesta.is_deleted == False)
            respuestas = query.all()
            session.expunge_all()
            return respuestas
        finally:
            session.close()

    @staticmethod
    def get_by_user_id(id_usuario, include_deleted=False):
        """Devuelve todas las respuestas publicadas por un usuario concreto."""
        session = get_session()
        try:
            query = session.query(Respuesta).filter(Respuesta.id_usuario == id_usuario)
            if not include_deleted:
                query = query.filter(Respuesta.is_deleted == False)
            respuestas = query.all()
            session.expunge_all()
            return respuestas
        finally:
            session.close()

    @staticmethod
    def get_by_id(id_respuesta):
        """Busca una respuesta por su ID."""
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
        """Marca una respuesta como eliminada (borrado logico)."""
        session = get_session()
        try:
            respuesta = session.query(Respuesta).filter_by(id_respuesta=id_respuesta).first()
            if respuesta:
                respuesta.is_deleted = True
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update(id_respuesta, contenido=None, imagen=None, es_mejor=None, is_deleted=None):
        """
        Actualiza los campos de una respuesta existente.
        
        Args:
            id_respuesta (int): ID de la respuesta a actualizar.
            contenido (str, optional): Nuevo contenido.
            imagen (str, optional): Nueva imagen.
            es_mejor (int, optional): Nuevo estado de mejor respuesta.
            is_deleted (bool, optional): Nuevo estado de borrado lógico.
            
        Returns:
            Respuesta: Objeto de la respuesta actualizada o None si no existe.
            
        Note:
            Se actualiza un campo solo si el usuario envía un dato nuevo (si el parámetro no es None), típicamente desde el JSON de la petición.
        """
        session = get_session()
        try:
            respuesta = session.query(Respuesta).filter_by(id_respuesta=id_respuesta).first()
            if not respuesta:
                return None

            if contenido is not None:
                respuesta.contenido_respuesta = contenido
            if imagen is not None:
                respuesta.imagen_respuesta = imagen
            if es_mejor is not None:
                respuesta.es_mejor_respuesta = es_mejor
            if is_deleted is not None:
                respuesta.is_deleted = is_deleted

            session.commit()
            session.refresh(respuesta)
            session.expunge(respuesta)
            return respuesta
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def get_by_user_paginated(id_usuario, limit, offset, include_deleted=False):
        """Obtiene las respuestas de un usuario de forma paginada."""
        session = get_session()
        try:
            query = session.query(Respuesta).filter(Respuesta.id_usuario == id_usuario)
            if not include_deleted:
                query = query.filter(Respuesta.is_deleted == False)
            respuestas = query.order_by(Respuesta.fecha_respuesta.desc())\
                .limit(limit).offset(offset).all()
            session.expunge_all()
            return respuestas
        finally:
            session.close()

    @staticmethod
    def count_by_user(id_usuario, include_deleted=False):
        """Cuenta el total de respuestas publicadas por un usuario."""
        session = get_session()
        try:
            query = session.query(Respuesta).filter(Respuesta.id_usuario == id_usuario)
            if not include_deleted:
                query = query.filter(Respuesta.is_deleted == False)
            return query.count()
        finally:
            session.close()