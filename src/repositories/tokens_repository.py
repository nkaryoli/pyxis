from src.extensions import get_session
from src.models.tokens import HistoricoTokens

class TokensRepository:

    @staticmethod
    def create(tokens, motivo, trimestre, id_usuario):
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
        session = get_session()
        try:
            historial = session.query(HistoricoTokens).filter_by(id_usuario=id_usuario).all()
            session.expunge_all()
            return historial
        finally:
            session.close()
            
    @staticmethod
    def delete(id_tokens):
        session = get_session()
        try:
            # Buscamos el registro en la tabla física HISTORICO_TOKENS
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
        session = get_session()
        try:
            # Hace un SELECT * FROM HISTORICO_TOKENS
            todos_los_tokens = session.query(HistoricoTokens).all()
            session.expunge_all()
            return todos_los_tokens
        finally:
            session.close()