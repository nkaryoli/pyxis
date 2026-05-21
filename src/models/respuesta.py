from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.extensions import Base

class Respuesta(Base):
    __tablename__ = 'respuestas'
    
    id_respuesta = Column(Integer, primary_key=True, autoincrement=True)
    contenido_respuesta = Column(Text, nullable=False)
    fecha_respuesta = Column(DateTime, default=datetime.utcnow)
    id_post = Column(Integer, nullable=False)
    id_usuario = Column(Integer, nullable=False)
    es_mejor_respuesta = Column(Integer, default=0) 
    imagen_respuesta = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Respuesta {self.id_respuesta} del Post {self.id_post}>"

    