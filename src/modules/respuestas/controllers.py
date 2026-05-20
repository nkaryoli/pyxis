# Coloca este import arriba junto a los demás servicios
from src.services.respuesta_service import RespuestaService 

# ... (Tus rutas anteriores de posts y render_template se quedan igual) ...


# ==========================================
# --- ENDPOINTS API PARA RESPUESTAS     ---
# ==========================================

# --- 1. CREAR RESPUESTA (POST) ---
@posts.route('/api/posts/<int:id_post>/respuestas', methods=['POST'])
def crear_respuesta_api(id_post):
    datos = request.get_json()
    
    # Validación con las nuevas columnas
    if not datos or 'contenido_respuesta' not in datos or 'id_usuario' not in datos:
        return jsonify({"error": "Faltan campos obligatorios: contenido_respuesta o id_usuario"}), 400
        
    try:
        nueva = RespuestaService.crear_respuesta(
            id_post=id_post,
            id_usuario=datos['id_usuario'],
            contenido=datos['contenido_respuesta'],
            es_mejor=datos.get('es_mejor_respuesta', 0),
            imagen=datos.get('imagen_respuesta')
        )
        return jsonify({"mensaje": "Respuesta creada con éxito", "respuesta": nueva.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 2. GET RESPUESTAS POR ID_POST ---
@posts.route('/api/posts/<int:id_post>/respuestas', methods=['GET'])
def listar_respuestas_post_api(id_post):
    try:
        lista = RespuestaService.obtener_respuestas_de_post(id_post)
        return jsonify([r.to_dict() for r in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 3. GET RESPUESTAS POR ID_USUARIO ---
@posts.route('/api/users/<int:id_usuario>/respuestas', methods=['GET'])
def ver_respuestas_usuario_api(id_usuario):
    try:
        lista = RespuestaService.obtener_respuestas_de_usuario(id_usuario)
        return jsonify([r.to_dict() for r in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500