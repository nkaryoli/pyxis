from src.repositories.prueba_repository import PruebaRepository

class PruebaService:
    """Servicio de lógica de negocio para Prueba."""
    
    @staticmethod
    def obtener_todas_pruebas():
        """Obtiene todas las pruebas."""
        return PruebaRepository.get_all()
    
    @staticmethod
    def obtener_prueba(id_prueba):
        """Obtiene una prueba por ID."""
        prueba = PruebaRepository.get_by_id(id_prueba)
        if not prueba:
            raise ValueError(f"Prueba con ID {id_prueba} no encontrada")
        return prueba
    
    @staticmethod
    def crear_prueba(titulo, descripcion):
        """Crea una nueva prueba con validación."""
        if not titulo or len(titulo) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres")
        if not descripcion or len(descripcion) < 5:
            raise ValueError("La descripción debe tener al menos 5 caracteres")
        
        return PruebaRepository.create(titulo, descripcion)