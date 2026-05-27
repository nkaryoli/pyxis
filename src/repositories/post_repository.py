from datetime import datetime, timedelta
from src.extensions import get_session
from src.models.post import Post
from sqlalchemy.orm import selectinload

class PostRepository:
    """Repositorio de acceso a datos para la entidad Post."""

    @staticmethod
    def get_all():
        """Devuelve todos los posts ordenados por fecha de creación descendente."""
        session = get_session()
        try:
            posts = session.query(Post).options(
                selectinload(Post.respuestas_relacion),
                selectinload(Post.modulo),
            ).order_by(Post.fecha_creacion_post.desc()).all()
            session.expunge_all()
            return posts
        finally:
            session.close()

    @staticmethod
    def get_by_id(id_post):
        """Busca un post por su identificador."""
        session = get_session()
        try:
            post = session.query(Post).options(
                selectinload(Post.respuestas_relacion),
                selectinload(Post.modulo),
            ).filter_by(id_post=id_post).first()
            if post:
                session.expunge(post)
            return post
        finally:
            session.close()

    @staticmethod
    def get_by_user_id(id_usuario):
        """Devuelve todos los posts de un usuario concreto."""
        session = get_session()
        try:
            posts = session.query(Post).options(
                selectinload(Post.respuestas_relacion),
                selectinload(Post.modulo),
            ).filter_by(id_usuario=id_usuario).all()
            session.expunge_all()
            return posts
        finally:
            session.close()

    @staticmethod
    def create(titulo, contenido, id_usuario, codigo_modulo, imagen=None):
        """Crea un nuevo post y devuelve la entidad persistida."""
        session = get_session()
        try:
            nuevo_post = Post(
                titulo_post=titulo,
                contenido_post=contenido,
                id_usuario=id_usuario,
                codigo_modulo=codigo_modulo,
                imagen_post=imagen
            )
            session.add(nuevo_post)
            session.commit()
            session.refresh(nuevo_post)
            session.expunge(nuevo_post)
            return nuevo_post
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(id_post):
        """Elimina un post por su identificador y devuelve si la operación tuvo éxito."""
        session = get_session()
        try:
            post = session.query(Post).filter_by(id_post=id_post).first()
            if post:
                session.delete(post)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update(id_post, titulo=None, contenido=None, codigo_modulo=None, imagen=None, fecha_creacion=None):
        """Actualiza los campos enviados de un post existente."""
        session = get_session()
        try:
            post = session.query(Post).filter_by(id_post=id_post).first()
            
            if not post:
                return None

            if titulo is not None:
                post.titulo_post = titulo
            if contenido is not None:
                post.contenido_post = contenido
            if codigo_modulo is not None:
                post.codigo_modulo = codigo_modulo
            if imagen is not None:
                post.imagen_post = imagen
            if fecha_creacion is not None: 
                post.fecha_creacion_post = fecha_creacion 

            session.commit()
            session.refresh(post)
            session.expunge(post)
            return post
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    @staticmethod
    def get_by_modulo_code(codigo_modulo):
        """Devuelve los posts asociados a un código de módulo."""
        session = get_session()
        try:
            codigo_limpio = (codigo_modulo or "").strip().upper()
            posts = session.query(Post).options(
                selectinload(Post.respuestas_relacion),
                selectinload(Post.modulo),
            ).filter_by(codigo_modulo=codigo_limpio).order_by(Post.fecha_creacion_post.desc()).all()
            session.expunge_all()
            return posts
        finally:
            session.close()
            
    @staticmethod
    def get_recent():
        """Devuelve los posts recientes publicados en los últimos días."""
        session = get_session()
        try:
            posts = session.query(Post).options(
                selectinload(Post.respuestas_relacion),
                selectinload(Post.modulo),
            ).order_by(Post.fecha_creacion_post.desc()).limit(10).all()
            session.expunge_all()
            limite_tres_dias = datetime.now() - timedelta(days=3)
            posts_filtrados = [
                p for p in posts 
                if p.fecha_creacion_post and p.fecha_creacion_post >= limite_tres_dias
            ]
            
            return posts_filtrados

        finally:
            session.close()
    
    
