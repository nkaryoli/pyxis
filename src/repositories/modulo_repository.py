from src.extensions import get_session
from src.models.modulo import Modulo
from sqlalchemy import func

class ModuloRepository:
    "Repositorio para operaciones CRUD de Modulo en la BD."

    @staticmethod
    def get_all():
        """Obtiene todos los modulos de la BD (Todos los Usuarios)."""
        session = get_session()
        try:
            return session.query(Modulo).all()
        finally:
            session.close()

    @staticmethod
    def get_by_codigo(codigo_modulo):
        """Obtiene un modulo en especifico de la BD (Todos los Usuarios)."""
        session = get_session()
        try:
            return session.query(Modulo).filter_by(codigo_modulo=codigo_modulo).first()
        finally:
            session.close()

    @staticmethod
    def get_by_name(nombre_modulo):
        """Busca un módulo por nombre ignorando mayúsculas/minúsculas."""
        session = get_session()
        try:
            modulo = session.query(Modulo).filter(
                func.lower(Modulo.nombre_asignatura) == nombre_modulo.lower()
            ).first()
            return modulo
        finally:
            session.close()

    @staticmethod
    def create(codigo_modulo, nombre_asignatura, curso_modulo):
        """Crea un nuevo modulo en la BD (Solo profesores y administradores)."""
        session = get_session()
        try:
            nuevo_modulo = Modulo(
                codigo_modulo=codigo_modulo,
                nombre_asignatura=nombre_asignatura,
                curso_modulo=curso_modulo
            )
            session.add(nuevo_modulo)
            session.commit()
            session.refresh(nuevo_modulo)
            return nuevo_modulo
        finally:
            session.close()

    @staticmethod
    def update(codigo_modulo, nuevo_nombre, nuevo_curso):
        """Actualiza un modulo existente en la BD (Solo profesores y administradores)."""
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(codigo_modulo=codigo_modulo).first()
            if modulo:
                modulo.nombre_asignatura = nuevo_nombre
                modulo.curso_modulo = nuevo_curso
                session.commit()
                session.refresh(modulo)
                return modulo
        finally:
            session.close()
    
    @staticmethod
    def delete(codigo_modulo):
        """Elimina un modulo de la BD (Solo profesores y administradores)."""
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(codigo_modulo=codigo_modulo).first()
            if modulo:
                session.delete(modulo)
                session.commit()
                return True
            return False
        finally:
            session.close()
            
