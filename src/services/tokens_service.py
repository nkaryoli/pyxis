from src.repositories.tokens_repository import TokensRepository

class TokensService:
    """Servicio de lógica de negocio para operaciones sobre el Historial de Tokens."""

    @staticmethod
    def registrar_tokens(tokens, motivo, trimestre, id_usuario):
        """
        Registra un movimiento en el historial de tokens.
        
        Args:
            tokens (int): Cantidad a modificar (positiva o negativa).
            motivo (str): Razón de la alteración.
            trimestre (str): Trimestre correspondiente al registro.
            id_usuario (int): ID del usuario afectado.
            
        Returns:
            HistoricoTokens: Objeto de registro de tokens creado.
        """
        return TokensRepository.create(tokens, motivo, trimestre, id_usuario)

    @staticmethod
    def obtener_historial_usuario(id_usuario):
        """Obtiene el historial completo de alteraciones de tokens de un usuario."""
        return TokensRepository.get_by_user_id(id_usuario)
    
    @staticmethod
    def eliminar_registro_tokens(id_tokens):
        """Elimina un registro específico del historial de tokens."""
        return TokensRepository.delete(id_tokens)

    @staticmethod
    def obtener_todos_los_tokens():
        """Obtiene el historial global de tokens de todo el sistema."""
        return TokensRepository.get_all()