from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from src.extensions import Base

class HistoricoTokens(Base):
    """Modelo que representa la tabla HISTORICO_TOKENS en la base de datos."""
    __tablename__ = 'HISTORICO_TOKENS'

    id_tokens = Column(Integer, primary_key=True, autoincrement=True)
    tokens = Column(Integer, nullable=False)
    fecha_tokens = Column(DateTime, default=func.current_timestamp())
    motivo = Column(String(255), nullable=False)
    trimestre = Column(String(50), nullable=False)
    id_usuario = Column(Integer, ForeignKey('USUARIOS.id_usuario'), nullable=False)

    def to_dict(self):
        """Devuelve un diccionario con los datos del registro histórico de tokens."""
        return {
            "id_tokens": self.id_tokens,
            "tokens": self.tokens,
            # Aseguramos la conversión a string si llega como objeto datetime
            "fecha_tokens": self.fecha_tokens.strftime('%Y-%m-%d %H:%M:%S') if hasattr(self.fecha_tokens, 'strftime') else str(self.fecha_tokens) if self.fecha_tokens else None,
            "motivo": self.motivo,
            "trimestre": self.trimestre,
            "id_usuario": self.id_usuario
        }