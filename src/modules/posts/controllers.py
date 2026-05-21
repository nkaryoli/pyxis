from flask import Blueprint, jsonify, request
from src.services.post_service import PostService

posts = Blueprint('posts', __name__)

# --- 1. LISTAR TODOS ---
@posts.route('/api/posts', methods=['GET'])
def listar_todos_api():
    try:
        lista = PostService.listar_todos()
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. ELIMINAR POR ID ---
@posts.route('/api/posts/<int:id_post>', methods=['DELETE'])
def eliminar_post_api(id_post):
    try:
        PostService.eliminar_post(id_post)
        return jsonify({"mensaje": f"Post {id_post} eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. CREAR ---
@posts.route('/api/posts', methods=['POST'])
def crear_post_api():
    datos = request.get_json()
    
    if not datos or 'titulo_post' not in datos or 'contenido_post' not in datos or 'id_usuario' not in datos:
        return jsonify({"error": "Faltan campos: titulo_post, contenido_post o id_usuario"}), 400
        
    try:
        nuevo = PostService.crear_post(
            titulo=datos['titulo_post'],
            contenido=datos['contenido_post'],
            id_usuario=datos['id_usuario'],
            codigo_modulo=datos.get('codigo_modulo'),
            imagen=datos.get('imagen_post')
        )
        return jsonify({"mensaje": "Post creado con éxito", "post": nuevo.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# --- 5. VER POSTS POR ID DE USUARIO ---
@posts.route('/api/users/<int:id_usuario>/posts', methods=['GET'])
def ver_posts_usuario_api(id_usuario):
    try:
        lista = PostService.ver_posts_por_usuario(id_usuario)
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500