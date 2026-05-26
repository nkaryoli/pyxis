from src.extensions import get_session
from src.models.post import Post

class PostRepository:

    @staticmethod
    def get_all():
        session = get_session()
        try:
            posts = session.query(Post).order_by(Post.fecha_creacion_post.desc()).all()
            session.expunge_all()
            return posts
        finally:
            session.close()

    @staticmethod
    def get_by_id(id_post):
        session = get_session()
        try:
            post = session.query(Post).filter_by(id_post=id_post).first()
            if post:
                session.expunge(post)
            return post
        finally:
            session.close()

    @staticmethod
    def get_by_user_id(id_usuario):
        session = get_session()
        try:
            posts = session.query(Post).filter_by(id_usuario=id_usuario).all()
            session.expunge_all()
            return posts
        finally:
            session.close()

    @staticmethod
    def create(titulo, contenido, id_usuario, codigo_modulo, imagen=None):
        session = get_session()
        try:
            nuevo_post = Post(
                titulo_post=titulo,
                contenido_post=contenido,
                id_usuario=id_usuario, # Corregido de id_usuario1 a id_usuario
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
    def update(id_post, titulo=None, contenido=None, codigo_modulo=None, imagen=None):
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
        session = get_session()
        try:
            codigo_limpio = (codigo_modulo or "").strip().upper()
            posts = session.query(Post).filter_by(codigo_modulo=codigo_limpio).order_by(Post.fecha_creacion_post.desc()).all()
            session.expunge_all()
            return posts
        finally:
            session.close()
            
    @staticmethod
    def get_recent():
        session = get_session()
        try:
            posts = session.query(Post).order_by(Post.fecha_creacion_post.desc()).limit(10).all()
            session.expunge_all()
            return posts
        finally:
            session.close()
    
    
