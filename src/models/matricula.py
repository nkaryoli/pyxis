from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.extensions import Base

class Matricula(Base):
    __tablename__ = 'MATRICULAS'
    
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), primary_key=True)
    codigo_modulo = Column(String(50), ForeignKey('modulos.codigo_modulo'), primary_key=True)
    
    fecha_inicio = Column(DateTime)
    fecha_final = Column(DateTime)
    

    def __repr__(self):
        return f'<Matricula {self.id_usuario} - {self.codigo_modulo}>'