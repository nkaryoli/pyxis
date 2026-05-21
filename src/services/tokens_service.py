from src.repositories.tokens_repository import TokensRepository

class TokensService:

    @staticmethod
    def registrar_tokens(tokens, motivo, trimestre, id_usuario):
        return TokensRepository.create(tokens, motivo, trimestre, id_usuario)

    @staticmethod
    def obtener_historial_usuario(id_usuario):
        return TokensRepository.get_by_user_id(id_usuario)
    
    @staticmethod
    def eliminar_registro_tokens(id_tokens):
        return TokensRepository.delete(id_tokens)