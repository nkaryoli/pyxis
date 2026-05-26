import pytest
from unittest.mock import patch, MagicMock
from src.services.tokens_service import TokensService



@patch('src.services.tokens_service.TokensRepository.create')
def test_registrar_tokens_exito(mock_create):
    # Configuración del Mock: simulamos el objeto que retornaría el repositorio
    mock_registro_esperado = MagicMock()
    mock_create.return_value = mock_registro_esperado

    # Datos de entrada para la prueba
    datos_test = {
        "tokens": 15,
        "motivo": "Participación en clase",
        "trimestre": "Segundo",
        "id_usuario": 101
    }

    # Ejecución del método del servicio
    resultado = TokensService.registrar_tokens(**datos_test)

    # Verificaciones (Asserts)
    # 1. Validamos que el método del repositorio se llamó exactamente una vez con los parámetros correctos
    mock_create.assert_called_once_with(15, "Participación en clase", "Segundo", 101)
    # 2. Validamos que el servicio retorna lo mismo que le entregó el repositorio
    assert resultado == mock_registro_esperado




@patch('src.services.tokens_service.TokensRepository.get_by_user_id')
def test_obtener_historial_usuario_exito(mock_get_by_user_id):
    # Configuración del Mock: simulamos una lista de registros
    mock_historial = [MagicMock(), MagicMock()]
    mock_get_by_user_id.return_value = mock_historial

    id_usuario_test = 101

    # Ejecución
    resultado = TokensService.obtener_historial_usuario(id_usuario_test)

    # Verificaciones
    mock_get_by_user_id.assert_called_once_with(id_usuario_test)
    assert resultado == mock_historial
    assert len(resultado) == 2



@patch('src.services.tokens_service.TokensRepository.delete')
def test_eliminar_registro_tokens_encontrado(mock_delete):
    # Caso 1: El registro existe y se elimina (retorna True)
    mock_delete.return_value = True
    id_tokens_test = 5

    resultado = TokensService.eliminar_registro_tokens(id_tokens_test)

    mock_delete.assert_called_once_with(id_tokens_test)
    assert resultado is True


@patch('src.services.tokens_service.TokensRepository.delete')
def test_eliminar_registro_tokens_no_encontrado(mock_delete):
    # Caso 2: El registro no existe en el repositorio (retorna False o None)
    mock_delete.return_value = False
    id_tokens_test = 999

    resultado = TokensService.eliminar_registro_tokens(id_tokens_test)

    mock_delete.assert_called_once_with(id_tokens_test)
    assert resultado is False




@patch('src.services.tokens_service.TokensRepository.get_all')
def test_obtener_todos_los_tokens_exito(mock_get_all):
    # Configuración del Mock: simulamos la lista global del repositorio
    mock_lista_global = [MagicMock(), MagicMock(), MagicMock()]
    mock_get_all.return_value = mock_lista_global

    resultado = TokensService.obtener_todos_los_tokens()

    mock_get_all.assert_called_once()
    assert resultado == mock_lista_global
    assert len(resultado) == 3