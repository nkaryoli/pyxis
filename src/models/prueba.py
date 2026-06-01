from sqlalchemy import Column, Integer, String
from src.extensions import Base

class Prueba(Base):
    """Modelo que representa la tabla de pruebas."""
    __tablename__ = 'pruebas'
    
    id_prueba = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(String(500), nullable=False)
    
    def __repr__(self):
        """Devuelve una representación en texto de la prueba."""
        return f"<Prueba {self.id_prueba}: {self.titulo}>"