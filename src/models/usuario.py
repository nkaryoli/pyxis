from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from src.extensions import Base

class Usuario(Base):
    """Modelo que representa la tabla USUARIOS en la base de datos."""
    __tablename__ = 'USUARIOS'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)  # <--- Sin unique=True
    email_usuario = Column(String(100), nullable=False, unique=True)
    password_usuario = Column(String(255), nullable=False)
    fecha_alta = Column(DateTime, server_default=func.now(), nullable=False)
    tokens = Column(Integer, default=0)
    rol = Column(String(50), nullable=False)
    imagen_usuario = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Usuario {self.id_usuario}: {self.username}>"