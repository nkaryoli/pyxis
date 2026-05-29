from src.models import Modulo, Matricula
from src.extensions import get_session

class MatriculaRepository:
    
    
    @staticmethod
    def get_modulos_para_usuario(usuario):
        """Devuelve los módulos matriculados si es alumno, o todos si es Admin/Profesor."""
        session = get_session()
        try:
            # Lógica de acceso por rol
            if usuario.rol in ['ADMINISTRADOR', 'PROFESOR']:
                # Devuelve todos los módulos del sistema
                return session.query(Modulo).all()
            else:
                # Devuelve solo los módulos en los que está matriculado
                return session.query(Modulo).join(
                    Matricula, Modulo.codigo_modulo == Matricula.codigo_modulo
                ).filter(Matricula.id_usuario == usuario.id_usuario).all()
        finally:
            session.close()
            
            
    @staticmethod
    def get_modulos_by_usuario(id_usuario):
        session = get_session() 
        try:
            return session.query(Modulo).join(
                Matricula, Modulo.codigo_modulo == Matricula.codigo_modulo
            ).filter(Matricula.id_usuario == id_usuario).all()
        finally:
            session.close() 
            
            
    @staticmethod
    def verificar_matricula(id_usuario, codigo_modulo):
        """Devuelve True si existe una matrícula para el usuario y módulo dados."""
        session = get_session()
        try:

            matricula = session.query(Matricula).filter_by(
                id_usuario=id_usuario, 
                codigo_modulo=codigo_modulo
            ).first()
            
            return matricula is not None
        finally:
            session.close()