from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from src.extensions import Base

class Post(Base):
    __tablename__ = 'POSTS'
    
    id_post = Column(Integer, primary_key=True, autoincrement=True)
    titulo_post = Column(String(150), nullable=False)
    contenido_post = Column(Text, nullable=False)
    fecha_creacion_post = Column(DateTime, default=datetime.now)
    id_usuario = Column(Integer, ForeignKey('USUARIOS.id_usuario'), nullable=True)
    codigo_modulo = Column(String(50), ForeignKey('MODULOS.codigo_modulo'), nullable=False) 
    imagen_post = Column(String(255), nullable=True)  
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    usuario = relationship("Usuario", backref="posts", lazy="joined") 
    modulo = relationship("Modulo", lazy="joined")
    respuestas_relacion = relationship("Respuesta", backref="post", lazy="selectin")
    
    def __repr__(self):
        return f"<Post {self.id_post}: {self.titulo_post}>"
    
    @property
    def created_at(self):
        return self.fecha_creacion_post

    @property
    def autor(self):
        from src.extensions import should_include_deleted
        if not self.usuario:
            return "Usuario Eliminado"
        if not self.usuario.is_active:
            if should_include_deleted():
                return f"Usuario Inactivo ({self.usuario.username})"
            return "Usuario Inactivo"
        return self.usuario.username

    @property
    def respuestas(self):
        return self.respuestas_relacion

    @property
    def respuestas_count(self):
        return len(self.respuestas)

    @property
    def modulo_nombre(self):
        if self.modulo and self.modulo.nombre_asignatura:
            return self.modulo.nombre_asignatura
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

 