from src.extensions import get_session
from src.models.prueba import Prueba

class PruebaRepository:
    """Repositorio para operaciones CRUD de Prueba en la BD."""
    
    @staticmethod
    def get_all():
        """Obtiene todas las pruebas de la BD."""
        session = get_session()
        try:
            return session.query(Prueba).all()
        finally:
            session.close()
    
    @staticmethod
    def get_by_id(id_prueba):
        """Obtiene una prueba por su ID."""
        session = get_session()
        try:
            return session.query(Prueba).filter_by(id_prueba=id_prueba).first()
        finally:
            session.close()
    
    @staticmethod
    def create(titulo, descripcion):
        """Crea una nueva prueba en la BD."""
        session = get_session()
        try:
            nueva_prueba = Prueba(titulo=titulo, descripcion=descripcion)
            session.add(nueva_prueba)
            session.commit()
            return nueva_prueba
        finally:
            session.close()