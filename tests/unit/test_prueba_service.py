"""
Tests unitarios para `PruebaService`.

Estos tests se centran en la capa de servicio y mockean el repositorio para
evitar acceder a la base de datos. Usamos `monkeypatch` para sustituir métodos
del repositorio por fakes pequeños, de modo que los tests sean rápidos y
deterministas. 
"""

import pytest
from src.services.prueba_service import PruebaService
from src.repositories.prueba_repository import PruebaRepository

def test_crear_prueba_valida(monkeypatch):
    """Verifica que `PruebaService.crear_prueba` envía datos válidos al
    repositorio y devuelve el objeto creado.

    Sustituimos `PruebaRepository.create` por `fake_create` que construye un
    objeto mínimo con los atributos que espera el servicio. Así evitamos usar
    modelos ORM o I/O de BD en tests unitarios.
    """
    created = []

    def fake_create(titulo, descripcion):
        class P:
            def __init__(self, id_prueba, titulo, descripcion):
                self.id_prueba = id_prueba
                self.titulo = titulo
                self.descripcion = descripcion

        p = P(1, titulo, descripcion)
        created.append(p)
        return p

    monkeypatch.setattr(PruebaRepository, "create", staticmethod(fake_create))
    service = PruebaService()
    res = service.crear_prueba("Python Basics", "Aprender Python")

    assert res.titulo == "Python Basics"
    assert created and created[0] is res


def test_crear_prueba_titulo_muy_corto():
    """Test de regla de negocio: el servicio debe rechazar títulos demasiado
    cortos (lanza `ValueError`).
    """
    service = PruebaService()
    titulo_corto = "a"
    with pytest.raises(ValueError):
        service.crear_prueba(titulo_corto, "Descripción")


def test_obtener_todas_pruebas(monkeypatch):
    """Asegura que `obtener_todas_pruebas` devuelve la lista que proporciona
    el repositorio. Stubamos `PruebaRepository.get_all` para no tocar la BD.
    """
    def fake_get_all():
        return [type("P", (), {"id_prueba": 1, "titulo": "T1", "descripcion": "D1"})()]

    monkeypatch.setattr(PruebaRepository, "get_all", staticmethod(fake_get_all))
    service = PruebaService()
    pruebas = service.obtener_todas_pruebas()
    assert len(pruebas) == 1