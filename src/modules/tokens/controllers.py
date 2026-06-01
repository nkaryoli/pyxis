from flask import Blueprint, jsonify, request
from src.services.tokens_service import TokensService

tokens = Blueprint('tokens', __name__)

@tokens.route('/api/tokens', methods=['POST'])
def crear_registro_tokens_api():
    """
    Endpoint API para registrar nuevos movimientos en el historial de tokens.
    
    Returns:
        JSON: Detalles del registro creado o mensaje de error si faltan campos obligatorios.
    """
    try:
        data = request.get_json()
        
        # Validamos campos obligatorios
        if not data or 'tokens' not in data or 'motivo' not in data or 'trimestre' not in data or 'id_usuario' not in data:
            return jsonify({"error": "Faltan campos requeridos: tokens, motivo, trimestre o id_usuario"}), 400

        nuevo_registro = TokensService.registrar_tokens(
            tokens=data['tokens'],
            motivo=data['motivo'],
            trimestre=data['trimestre'],
            id_usuario=data['id_usuario']
        )
        
        return jsonify({"mensaje": "Tokens registrados con éxito", "registro": nuevo_registro.to_dict()}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@tokens.route('/api/usuarios/<int:id_usuario>/tokens', methods=['GET'])
def ver_historial_tokens_api(id_usuario):
    """Endpoint API para ver todo el historial de tokens de un usuario en concreto."""
    try:
        lista = TokensService.obtener_historial_usuario(id_usuario)
        return jsonify([t.to_dict() for t in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@tokens.route('/api/tokens/<int:id_tokens>', methods=['DELETE'])
def eliminar_tokens_api(id_tokens):
    """
    Endpoint API para eliminar un registro específico del historial de tokens.
    
    Args:
        id_tokens (int): ID único del registro a borrar.
        
    Returns:
        JSON: Mensaje de éxito si fue eliminado, o código 403 si el rol no es adecuado.
        
    Note:
        Sólo administradores y profesores tienen permitido realizar esta acción.
    """
    try:
        usuario_rol = request.headers.get('X-User-Role') 
        
        if not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Role en los Headers."}), 401

        # REGLA DE SEGURIDAD: Solo profesores o administradores pueden alterar el histórico
        if usuario_rol not in ['ADMINISTRADOR', 'PROFESOR']:
            return jsonify({"error": "No tienes permisos para eliminar registros del histórico de tokens."}), 403

        eliminado = TokensService.eliminar_registro_tokens(id_tokens)

        if not eliminado:
            return jsonify({"error": f"No se encontró ningún registro de tokens con el ID {id_tokens}"}), 404
            
        return jsonify({"mensaje": f"Registro de tokens con ID {id_tokens} eliminado correctamente"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@tokens.route('/api/tokens', methods=['GET'])
def ver_todos_los_tokens_api():
    """
    Endpoint API global para obtener todos los registros de tokens del sistema.
    
    Returns:
        JSON: Lista completa del historial global de tokens en el sistema.
        
    Note:
        Restringido a roles ADMINISTRADOR y PROFESOR para evitar que los alumnos vean balances de terceros.
    """
    try:
        usuario_rol = request.headers.get('X-User-Role')
        
        if not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Role en los Headers."}), 401

        if usuario_rol not in ['ADMINISTRADOR', 'PROFESOR']:
            return jsonify({"error": "No tienes permisos para ver el listado global de tokens."}), 403

        lista_completa = TokensService.obtener_todos_los_tokens()
        return jsonify([t.to_dict() for t in lista_completa]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500