"""
Tests unitarios para `ModuloService`.

Estos tests se centran en la capa de servicio y mockean el repositorio para
evitar acceder a la base de datos. Usamos `monkeypatch` para sustituir métodos
del repositorio por fakes pequeños, garantizando pruebas rápidas y deterministas.
"""

import pytest
from src.services.modulo_service import ModuloService
from src.repositories.modulo_repository import ModuloRepository

class FakeModulo:
    def __init__(self, codigo_modulo, nombre_asignatura, curso_modulo):
        self.codigo_modulo = codigo_modulo
        self.nombre_asignatura = nombre_asignatura
        self.curso_modulo = curso_modulo


def test_obtener_todos_los_modulos(monkeypatch):
    """Asegura que devuelve la lista proporcionada por el repositorio."""
    def fake_get_all(*args, **kwargs):
        return [FakeModulo("PROG", "Programación", "1DAM")]

    monkeypatch.setattr(ModuloRepository, "get_all", staticmethod(fake_get_all))
    modulos = ModuloService.obtener_todos_los_modulos()
    
    assert len(modulos) == 1
    assert modulos[0].codigo_modulo == "PROG"

def test_obtener_modulo_por_codigo_valido(monkeypatch):
    """Verifica que devuelve un módulo si el código existe."""
    def fake_get_by_codigo(codigo, *args, **kwargs):
        return FakeModulo(codigo, "Sistemas", "1SMR")

    monkeypatch.setattr(ModuloRepository, "get_by_codigo", staticmethod(fake_get_by_codigo))
    modulo = ModuloService.obtener_modulo_por_codigo("SIST")
    
    assert modulo.codigo_modulo == "SIST"

def test_obtener_modulo_codigo_vacio():
    """Valida que rechaza códigos vacíos al buscar."""
    with pytest.raises(ValueError, match="no puede estar vacío"):
        ModuloService.obtener_modulo_por_codigo("")

def test_obtener_modulo_no_encontrado(monkeypatch):
    """Valida que lanza error si el módulo no existe."""
    monkeypatch.setattr(ModuloRepository, "get_by_codigo", staticmethod(lambda x, *args, **kwargs: None))
    with pytest.raises(ValueError, match="no encontrado"):
        ModuloService.obtener_modulo_por_codigo("FAKE")


def test_crear_nuevo_modulo_valido(monkeypatch):
    """Verifica la creación exitosa de un módulo con roles autorizados."""
    created = []

    def fake_get_by_codigo(codigo, *args, **kwargs):
        return None  # Simulamos que no existe para que permita crearlo

    def fake_create(codigo, nombre, curso):
        m = FakeModulo(codigo, nombre, curso)
        created.append(m)
        return m

    monkeypatch.setattr(ModuloRepository, "get_by_codigo", staticmethod(fake_get_by_codigo))
    monkeypatch.setattr(ModuloRepository, "create", staticmethod(fake_create))
    
    res = ModuloService.crear_nuevo_modulo("BBDD", "Bases de Datos", "1DAM", "PROFESOR")

    assert res.codigo_modulo == "BBDD"
    assert created and created[0] is res

def test_crear_nuevo_modulo_rol_denegado():
    """Asegura que roles no autorizados (ej. ALUMNO) no pueden crear módulos."""
    with pytest.raises(ValueError, match="Acceso denegado"):
        ModuloService.crear_nuevo_modulo("BBDD", "Bases de Datos", "1DAM", "ALUMNO")

def test_crear_nuevo_modulo_campos_vacios():
    """Valida que rechaza la creación si faltan campos."""
    with pytest.raises(ValueError, match="obligatorios"):
        ModuloService.crear_nuevo_modulo("", "Bases de Datos", "1DAM", "ADMINISTRADOR")

def test_crear_nuevo_modulo_longitudes_cortas():
    """Valida que se respeten las longitudes mínimas de los campos."""
    with pytest.raises(ValueError, match="al menos 3 caracteres"):
        ModuloService.crear_nuevo_modulo("BD", "Bases de Datos", "1DAM", "PROFESOR")

def test_crear_nuevo_modulo_ya_existente(monkeypatch):
    """Valida que no permite crear si el código ya existe en BD."""
    monkeypatch.setattr(ModuloRepository, "get_by_codigo", staticmethod(lambda x, *args, **kwargs: FakeModulo("PROG", "Prog", "1")))
    with pytest.raises(ValueError, match="ya está registrado"):
        ModuloService.crear_nuevo_modulo("PROG", "Programación", "1DAM", "PROFESOR")


def test_modificar_modulo_valido(monkeypatch):
    """Verifica que se actualiza el módulo correctamente."""
    def fake_get_by_codigo(codigo, *args, **kwargs):
        return FakeModulo(codigo, "Antiguo", "1DAM")

    def fake_update(codigo, nombre, curso, *args, **kwargs):
        return FakeModulo(codigo, nombre, curso)

    monkeypatch.setattr(ModuloRepository, "get_by_codigo", staticmethod(fake_get_by_codigo))
    monkeypatch.setattr(ModuloRepository, "update", staticmethod(fake_update))

    res = ModuloService.modificar_modulo("PROG", "Nuevo Nombre", "2DAM", "ADMINISTRADOR")
    assert res.nombre_asignatura == "Nuevo Nombre"
    assert res.curso_modulo == "2DAM"

def test_modificar_modulo_no_existente(monkeypatch):
    """Evita modificar un módulo que no existe."""
    monkeypatch.setattr(ModuloRepository, "get_by_codigo", staticmethod(lambda x, *args, **kwargs: None))
    with pytest.raises(ValueError, match="no existe"):
        ModuloService.modificar_modulo("PROG", "Nuevo Nombre", "2DAM", "PROFESOR")


def test_eliminar_modulo_existente_valido(monkeypatch):
    """Verifica que llama al repositorio para borrar si todo es correcto."""
    deleted_called = []

    def fake_get_by_codigo(codigo, *args, **kwargs):
        return FakeModulo(codigo, "Antiguo", "1DAM")

    def fake_delete(codigo):
        deleted_called.append(codigo)
        return True

    monkeypatch.setattr(ModuloRepository, "get_by_codigo", staticmethod(fake_get_by_codigo))
    monkeypatch.setattr(ModuloRepository, "delete", staticmethod(fake_delete))

    ModuloService.eliminar_modulo_existente("PROG", "ADMINISTRADOR")
    assert "PROG" in deleted_called

def test_eliminar_modulo_rol_denegado():
    """Impide borrar módulos si no se tienen los permisos."""
    with pytest.raises(ValueError, match="Acceso denegado"):
        ModuloService.eliminar_modulo_existente("PROG", "ALUMNO")