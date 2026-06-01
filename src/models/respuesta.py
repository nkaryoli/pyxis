from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from src.extensions import Base

class Respuesta(Base):
    """Modelo que representa la tabla RESPUESTAS en la base de datos."""
    __tablename__ = 'RESPUESTAS'
    
    id_respuesta = Column(Integer, primary_key=True, autoincrement=True)
    contenido_respuesta = Column(Text, nullable=False)
    fecha_respuesta = Column(DateTime, default=datetime.utcnow)
    id_post = Column(Integer, ForeignKey('POSTS.id_post'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('USUARIOS.id_usuario'), nullable=True)
    es_mejor_respuesta = Column(Integer, default=0) 
    imagen_respuesta = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

    usuario = relationship("Usuario", backref="respuestas", lazy="joined")
    
    def __repr__(self):
        """Devuelve una representación en texto de la respuesta."""
        return f"<Respuesta {self.id_respuesta} del Post {self.id_post}>"
    
    @property
    def contenido(self):
        """Obtiene el contenido de la respuesta."""
        return self.contenido_respuesta

    @property
    def created_at(self):
        """Obtiene la fecha de creación de la respuesta."""
        return self.fecha_respuesta

    @property
    def autor(self):
        """Obtiene el nombre de usuario del autor de la respuesta, manejando eliminados o inactivos."""
        from src.extensions import should_include_deleted
        if not self.usuario:
            return "Usuario Eliminado"
        if not self.usuario.is_active:
            if should_include_deleted():
                return f"Usuario Inactivo ({self.usuario.username})"
            return "Usuario Inactivo"
        return self.usuario.username
    
    @property
    def mejor(self):
        """Indica si la respuesta fue marcada como la mejor respuesta."""
        return bool(self.es_mejor_respuesta)
    
    def to_dict(self):
        """Devuelve un diccionario con los datos de la respuesta."""
        return {
            "id_respuesta": self.id_respuesta,
            "contenido_respuesta": self.contenido_respuesta,
            "imagen_respuesta": self.imagen_respuesta,
            "id_post": self.id_post,
            "id_usuario": self.id_usuario,
            "username_autor": self.autor,
            "fecha_respuesta": self.fecha_respuesta.isoformat() if self.fecha_respuesta else None
        }