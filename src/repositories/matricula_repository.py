from src.extensions import get_session
from src.models import Modulo, Matricula

class MatriculaRepository:
    """Repositorio para operaciones de base de datos de la tabla MATRICULAS."""

    @staticmethod
    def get_modulos_para_usuario(usuario):
        """
        Devuelve los módulos matriculados si es alumno, o todos si es Admin/Profesor.

        Args:
            usuario (Usuario): El objeto usuario solicitante.

        Returns:
            list: Listado de objetos Modulo.
        """
        session = get_session()
        try:
            if usuario.rol in ['ADMINISTRADOR', 'PROFESOR']:
                return session.query(Modulo).all()
            else:
                return session.query(Modulo).join(
                    Matricula, Modulo.codigo_modulo == Matricula.codigo_modulo
                ).filter(Matricula.id_usuario == usuario.id_usuario).all()
        finally:
            session.close()

    @staticmethod
    def get_modulos_by_usuario(id_usuario):
        """
        Devuelve los módulos en los que está matriculado un usuario.

        Args:
            id_usuario (int): ID del usuario.

        Returns:
            list: Listado de objetos Modulo.
        """
        session = get_session() 
        try:
            return session.query(Modulo).join(
                Matricula, Modulo.codigo_modulo == Matricula.codigo_modulo
            ).filter(Matricula.id_usuario == id_usuario).all()
        finally:
            session.close() 

    @staticmethod
    def verificar_matricula(id_usuario, codigo_modulo):
        """
        Devuelve True si existe una matrícula activa para el usuario y módulo.

        Args:
            id_usuario (int): ID del usuario.
            codigo_modulo (str): Código del módulo.

        Returns:
            bool: True si la matrícula existe.
        """
        session = get_session()
        try:
            matricula = session.query(Matricula).filter_by(
                id_usuario=id_usuario, 
                codigo_modulo=codigo_modulo
            ).first()
            return matricula is not None
        finally:
            session.close()

    @staticmethod
    def get_by_usuario_id(id_usuario):
        """
        Obtiene todas las matrículas asociadas a un usuario concreto.

        Args:
            id_usuario (int): ID del usuario.

        Returns:
            list: Listado de objetos Matricula.
        """
        session = get_session()
        try:
            return session.query(Matricula).filter_by(id_usuario=id_usuario).all()
        finally:
            session.close()

    @staticmethod
    def create(id_usuario, codigo_modulo, fecha_inicio, fecha_final):
        """
        Crea e inserta una nueva matrícula en la base de datos.

        Args:
            id_usuario (int): ID del usuario.
            codigo_modulo (str): Código del módulo.
            fecha_inicio (datetime): Fecha de inicio de la vigencia.
            fecha_final (datetime): Fecha final de la vigencia.

        Returns:
            Matricula: Objeto de la matrícula creada.
        """
        session = get_session()
        try:
            nueva_matricula = Matricula(
                id_usuario=id_usuario,
                codigo_modulo=codigo_modulo,
                fecha_inicio=fecha_inicio,
                fecha_final=fecha_final
            )
            session.add(nueva_matricula)
            session.commit()
            session.refresh(nueva_matricula)
            return nueva_matricula
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def delete_all_by_usuario_id(id_usuario):
        """
        Elimina todas las matrículas registradas para un usuario.

        Args:
            id_usuario (int): ID del usuario.

        Returns:
            bool: True si la operación se realizó correctamente.
        """
        session = get_session()
        try:
            session.query(Matricula).filter_by(id_usuario=id_usuario).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_alumnos_by_modulo(codigo_modulo):
        """
        Obtiene todos los usuarios con rol ALUMNO matriculados en un módulo concreto.

        Args:
            codigo_modulo (str): Código del módulo.

        Returns:
            list: Listado de objetos Usuario.
        """
        from src.models.usuario import Usuario
        session = get_session()
        try:
            return session.query(Usuario).join(
                Matricula, Usuario.id_usuario == Matricula.id_usuario
            ).filter(
                Matricula.codigo_modulo == codigo_modulo,
                Usuario.rol == 'ALUMNO'
            ).all()
        finally:
            session.close()

    @staticmethod
    def get_conteo_alumnos_por_modulo(codigo_modulo):
        """
        Obtiene la cantidad de alumnos matriculados en un módulo concreto.

        Args:
            codigo_modulo (str): Código del módulo.

        Returns:
            int: Cantidad de alumnos matriculados.
        """
        session = get_session()
        try:
            return session.query(Matricula).filter_by(codigo_modulo=codigo_modulo).count()
        finally:
            session.close()
