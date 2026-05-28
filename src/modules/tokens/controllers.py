from flask import Blueprint, jsonify, request
from src.services.tokens_service import TokensService

tokens = Blueprint('tokens', __name__)

# --- 1. CREAR REGISTRO DE TOKENS (POST) ---
@tokens.route('/api/tokens', methods=['POST'])
def crear_registro_tokens_api():
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


# --- 2. VER HISTORIAL DE UN USUARIO (GET) ---
@tokens.route('/api/usuarios/<int:id_usuario>/tokens', methods=['GET'])
def ver_historial_tokens_api(id_usuario):
    try:
        lista = TokensService.obtener_historial_usuario(id_usuario)
        return jsonify([t.to_dict() for t in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# --- 3. ELIMINAR REGISTRO DE TOKENS POR ID (DELETE) ---
@tokens.route('/api/tokens/<int:id_tokens>', methods=['DELETE'])
def eliminar_tokens_api(id_tokens):
    try:
        # Extraemos el rol desde las cabeceras de seguridad de Postman
        usuario_rol = request.headers.get('X-User-Role') # 'ALUMNO', 'PROFESOR', 'ADMINISTRADOR'
        
        if not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Role en los Headers."}), 401

        # REGLA DE SEGURIDAD: Solo profesores o administradores pueden alterar el histórico
        if usuario_rol not in ['ADMINISTRADOR', 'PROFESOR']:
            return jsonify({"error": "No tienes permisos para eliminar registros del histórico de tokens."}), 403

        # Si pasa el filtro, procedemos a borrar
        eliminado = TokensService.eliminar_registro_tokens(id_tokens)

        if not eliminado:
            return jsonify({"error": f"No se encontró ningún registro de tokens con el ID {id_tokens}"}), 404
            
        return jsonify({"mensaje": f"Registro de tokens con ID {id_tokens} eliminado correctamente"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
# --- 4. VER TODOS LOS TOKENS DE LA PLATAFORMA (GET GLOBAL) ---
@tokens.route('/api/tokens', methods=['GET'])
def ver_todos_los_tokens_api():
    try:
        # Extraemos el rol desde las cabeceras de Postman por seguridad
        usuario_rol = request.headers.get('X-User-Role')
        
        if not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Role en los Headers."}), 401

        # REGLA DE SEGURIDAD: Un alumno no debe ver los movimientos de tokens de sus compañeros
        if usuario_rol not in ['ADMINISTRADOR', 'PROFESOR']:
            return jsonify({"error": "No tienes permisos para ver el listado global de tokens."}), 403

        # Si pasa el filtro, obtenemos la lista completa
        lista_completa = TokensService.obtener_todos_los_tokens()
        return jsonify([t.to_dict() for t in lista_completa]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500