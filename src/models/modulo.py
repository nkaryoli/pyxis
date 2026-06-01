from sqlalchemy import Column, Integer, String, Boolean
from src.extensions import Base

class Modulo(Base):
    """Modelo que representa la tabla MODULOS en la base de datos."""
    __tablename__ = 'MODULOS'

    codigo_modulo = Column(String(50), primary_key=True)
    nombre_asignatura= Column(String(100), nullable=False, unique=True)
    curso_modulo = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        """Devuelve una representación en texto del módulo."""
        return f"<Modulo {self.codigo_modulo}: {self.nombre_asignatura}>"