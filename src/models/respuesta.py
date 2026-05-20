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
    es_mejor_respuesta = Column(Integer, default=0) # Almacena 1 o 0 (o TinyInt)
    imagen_respuesta = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Respuesta {self.id_respuesta} del Post {self.id_post}>"

    def to_dict(self):
        return {
            "id_respuesta": self.id_respuesta,
            "contenido_respuesta": self.contenido_respuesta,
            "fecha_respuesta": self.fecha_respuesta.isoformat() if self.fecha_respuesta else None,
            "id_post": self.id_post,
            "id_usuario": self.id_usuario,
            "es_mejor_respuesta": self.es_mejor_respuesta,
            "imagen_respuesta": self.imagen_respuesta
        }