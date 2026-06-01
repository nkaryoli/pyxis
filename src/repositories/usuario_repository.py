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
        """
        Inserta un nuevo usuario en la base de datos.
        
        Args:
            username (str): Nombre de usuario (se guardará recortado/limpio según la lógica previa).
            email (str): Correo electrónico del usuario.
            password (str): Contraseña hasheada.
            rol (str): Rol del usuario (ALUMNO, PROFESOR, ADMINISTRADOR).
            
        Returns:
            Usuario: El objeto del usuario recién creado.
            
        Note:
            Se establece el valor inicial de tokens por defecto a 0.
            Se refresca la sesión al final para obtener el ID generado automáticamente y la fecha_alta por defecto.
        """
        session = get_session()
        try:
            nuevo_usuario = Usuario(                
                username=username,
                email_usuario=email,
                password_usuario=password,
                rol=rol,
                tokens=0
            )
            session.add(nuevo_usuario)
            session.commit()
            session.refresh(nuevo_usuario)
            return nuevo_usuario
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def update(id_usuario, datos):
        """
        Actualiza datos de un usuario existente.
        
        Args:
            id_usuario (int): ID del usuario a actualizar.
            datos (dict): Diccionario con los campos y nuevos valores a actualizar.
            
        Returns:
            Usuario: El objeto de usuario actualizado, o None si no existe.
            
        Note:
            Ignora la actualización del campo clave 'id_usuario'.
            Se recarga el objeto con session.refresh() antes de cerrar la sesión para poder usarlo después en el controlador sin problemas de LazyLoading.
        """
        session = get_session()
        try:
            usuario = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
            if usuario:
                for clave, valor in datos.items():
                    if hasattr(usuario, clave) and clave != 'id_usuario':
                        setattr(usuario, clave, valor)
                session.commit()
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