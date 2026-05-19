from sqlalchemy import Column, Integer, String
from src.extensions import Base

class Prueba(Base):
    __tablename__ = 'pruebas'
    
    id_prueba = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(String(500), nullable=False)
    
    def __repr__(self):
        return f"<Prueba {self.id_prueba}: {self.titulo}>"