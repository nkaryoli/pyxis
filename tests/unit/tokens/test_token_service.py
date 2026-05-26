import pytest
from unittest.mock import patch, MagicMock
from src.services.tokens_service import TokensService



@patch('src.services.tokens_service.TokensRepository.create')
def test_registrar_tokens_exito(mock_create):
    mock_registro_esperado = MagicMock()
    mock_create.return_value = mock_registro_esperado

    datos_test = {
        "tokens": 15,
        "motivo": "Participación en clase",
        "trimestre": "Segundo",
        "id_usuario": 101
    }

    resultado = TokensService.registrar_tokens(**datos_test)
    mock_create.assert_called_once_with(15, "Participación en clase", "Segundo", 101)
    assert resultado == mock_registro_esperado




@patch('src.services.tokens_service.TokensRepository.get_by_user_id')
def test_obtener_historial_usuario_exito(mock_get_by_user_id):
    mock_historial = [MagicMock(), MagicMock()]
    mock_get_by_user_id.return_value = mock_historial

    id_usuario_test = 101
    
    resultado = TokensService.obtener_historial_usuario(id_usuario_test)

    mock_get_by_user_id.assert_called_once_with(id_usuario_test)
    assert resultado == mock_historial
    assert len(resultado) == 2



@patch('src.services.tokens_service.TokensRepository.delete')
def test_eliminar_registro_tokens_encontrado(mock_delete):
    mock_delete.return_value = True
    id_tokens_test = 5

    resultado = TokensService.eliminar_registro_tokens(id_tokens_test)

    mock_delete.assert_called_once_with(id_tokens_test)
    assert resultado is True


@patch('src.services.tokens_service.TokensRepository.delete')
def test_eliminar_registro_tokens_no_encontrado(mock_delete):
    mock_delete.return_value = False
    id_tokens_test = 999

    resultado = TokensService.eliminar_registro_tokens(id_tokens_test)

    mock_delete.assert_called_once_with(id_tokens_test)
    assert resultado is False




@patch('src.services.tokens_service.TokensRepository.get_all')
def test_obtener_todos_los_tokens_exito(mock_get_all):
    mock_lista_global = [MagicMock(), MagicMock(), MagicMock()]
    mock_get_all.return_value = mock_lista_global

    resultado = TokensService.obtener_todos_los_tokens()

    mock_get_all.assert_called_once()
    assert resultado == mock_lista_global
    assert len(resultado) == 3