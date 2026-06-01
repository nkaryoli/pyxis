from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.extensions import Base

class Matricula(Base):
    """Modelo que representa la tabla MATRICULAS en la base de datos."""
    __tablename__ = 'MATRICULAS'

    id_usuario = Column(Integer, ForeignKey('USUARIOS.id_usuario', ondelete='CASCADE'), primary_key=True)
    codigo_modulo = Column(String(50), ForeignKey('MODULOS.codigo_modulo', ondelete='CASCADE'), primary_key=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_final = Column(DateTime, nullable=False)

    def __repr__(self):
        """Devuelve una representación en texto de la matrícula."""
        return f"<Matricula id_usuario={self.id_usuario} codigo_modulo={self.codigo_modulo}>"
