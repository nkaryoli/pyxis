from src.extensions import get_session
from src.models.tokens import HistoricoTokens

class TokensRepository:
    """Repositorio para operaciones CRUD sobre la tabla HISTORICO_TOKENS."""

    @staticmethod
    def create(tokens, motivo, trimestre, id_usuario):
        """Crea un nuevo registro en el historial de tokens."""
        session = get_session()
        try:
            nuevo_registro = HistoricoTokens(
                tokens=tokens,
                motivo=motivo,
                trimestre=trimestre,
                id_usuario=id_usuario
            )
            session.add(nuevo_registro)
            session.commit()
            session.refresh(nuevo_registro)
            session.expunge(nuevo_registro)
            return nuevo_registro
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_by_user_id(id_usuario):
        """Obtiene el historial de tokens de un usuario específico."""
        session = get_session()
        try:
            historial = session.query(HistoricoTokens).filter_by(id_usuario=id_usuario).all()
            session.expunge_all()
            return historial
        finally:
            session.close()
            
    @staticmethod
    def delete(id_tokens):
        """
        Elimina un registro del historial de tokens por su ID.
        
        Args:
            id_tokens (int): ID del registro de tokens.
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró.
            
        Note:
            Buscamos el registro directamente en la tabla física HISTORICO_TOKENS y realizamos un borrado físico (no lógico).
        """
        session = get_session()
        try:
            registro = session.query(HistoricoTokens).filter_by(id_tokens=id_tokens).first()
            if registro:
                session.delete(registro)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def get_all():
        """
        Obtiene todos los registros del historial de tokens.
        
        Returns:
            list[HistoricoTokens]: Lista de todos los movimientos de tokens.
            
        Note:
            Hace un SELECT * FROM HISTORICO_TOKENS sin filtros.
        """
        session = get_session()
        try:
            todos_los_tokens = session.query(HistoricoTokens).all()
            session.expunge_all()
            return todos_los_tokens
        finally:
            session.close()