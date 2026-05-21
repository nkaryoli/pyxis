from flask import Blueprint, jsonify, request
from src.services.tokens_service import TokensService

# 1. Definimos el Blueprint con el nombre que busca tu __init__.py
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