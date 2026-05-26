from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.extensions import Base

class Respuesta(Base):
    __tablename__ = 'RESPUESTAS'
    
    id_respuesta = Column(Integer, primary_key=True, autoincrement=True)
    contenido_respuesta = Column(Text, nullable=False)
    fecha_respuesta = Column(DateTime, default=datetime.utcnow)
    id_post = Column(Integer, ForeignKey('POSTS.id_post'), nullable=False)
    id_usuario = Column(Integer, nullable=False)
    es_mejor_respuesta = Column(Integer, default=0) 
    imagen_respuesta = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<Respuesta {self.id_respuesta} del Post {self.id_post}>"
    
    
    @property
    def contenido(self):
        return self.contenido_respuesta

    @property
    def created_at(self):
        return self.fecha_respuesta

    @property
    def autor(self):
        return f"Usuario {self.id_usuario}"

    @property
    def mejor(self):
        return bool(self.es_mejor_respuesta)
    
    
    def to_dict(self):
        return {
            "id_respuesta": self.id_respuesta,
            "contenido_respuesta": self.contenido_respuesta,
            "id_post": self.id_post,
            "id_usuario": self.id_usuario
            
        }

    