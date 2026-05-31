from src.extensions import get_session
from src.models.usuario import Usuario

class UsuarioRepository:
    """Repositorio para operaciones CRUD de la tabla USUARIOS."""

    @staticmethod
    def get_all():
        """Obtiene todos los usuarios de la base de datos."""
        session = get_session()
        try:
            return session.query(Usuario).order_by(Usuario.id_usuario.asc()).all()
        finally:
            session.close()
    
    @staticmethod
    def get_by_id(id_usuario):
        """Busca un usuario por su clave primaria."""
        session = get_session()
        try:
            return session.query(Usuario).filter_by(id_usuario=id_usuario).first()
        finally:
            session.close()

    @staticmethod
    def get_by_username(username):
        """Busca un usuario por su nombre de usuario."""
        session = get_session()
        try:
            return session.query(Usuario).filter_by(username=username).first()
        finally:
            session.close()

    @staticmethod
    def get_by_email(email):
        """Busca un usuario por su email."""
        session = get_session()
        try:
            return session.query(Usuario).filter_by(email_usuario=email).first()
        finally:
            session.close()

    @staticmethod
    def create(username, email, password, rol):
        """Inserta un nuevo usuario incluyendo el username generado."""
        session = get_session()
        try:
            nuevo_usuario = Usuario(                
                username=username, # <--- Ahora guardamos el nombre recortado
                email_usuario=email,
                password_usuario=password,
                rol=rol,
                tokens=0 # Valor inicial por defecto
            )
            session.add(nuevo_usuario)
            session.commit()
            # Refrescamos para obtener el ID generado y la fecha_alta por defecto
            session.refresh(nuevo_usuario)
            return nuevo_usuario
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update(id_usuario, datos):
        """Actualiza datos de un usuario existente."""
        session = get_session()
        try:
            usuario = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
            if usuario:
                for clave, valor in datos.items():
                    if hasattr(usuario, clave) and clave != 'id_usuario':
                        setattr(usuario, clave, valor)
                session.commit()
                # Recargamos el objeto antes de cerrar la sesión para poder usarlo después
                session.refresh(usuario)
                return usuario
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete(id_usuario):
        """Desactiva un usuario de la base de datos (borrado lógico)."""
        session = get_session()
        try:
            usuario = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
            if usuario:
                usuario.is_active = False
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()