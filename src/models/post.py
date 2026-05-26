from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.extensions import Base

class Post(Base):
    __tablename__ = 'POSTS'
    
    id_post = Column(Integer, primary_key=True, autoincrement=True)
    titulo_post = Column(String(150), nullable=False)
    contenido_post = Column(Text, nullable=False)
    fecha_creacion_post = Column(DateTime, default=datetime.now)
    id_usuario = Column(Integer, nullable=False)
    codigo_modulo = Column(String(50), nullable=True) 
    imagen_post = Column(String(255), nullable=True)   
    
    def __repr__(self):
        return f"<Post {self.id_post}: {self.titulo_post}>"
    
    @property
    def created_at(self):
        return self.fecha_creacion_post

    @property
    def autor(self):
        return f"Usuario {self.id_usuario}"

    @property
    def respuestas(self):
        return []

    @property
    def respuestas_count(self):
        return len(self.respuestas)

    @property
    def modulo_nombre(self):
        return self.codigo_modulo or "General"

    @property
    def modulo_slug(self):
        return (self.codigo_modulo or "").lower().strip()
    
    def to_dict(self):
        return {
            "id_post": self.id_post,
            "titulo_post": self.titulo_post,
            "contenido_post": self.contenido_post,
            "id_usuario": self.id_usuario,
            "codigo_modulo": self.codigo_modulo,
            "imagen_post": self.imagen_post,
            "fecha_creacion": self.fecha_creacion_post.isoformat() if self.fecha_creacion_post else None
        }

 