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
    try:

        data = request.get_json() 
        
        # Ahora que 'data' ya existe, Flask podrá leer los campos del JSON:
        nuevo_post = PostService.crear_post(
            titulo=data.get('titulo_post'),
            contenido=data.get('contenido_post'),
            id_usuario=data.get('id_usuario'),
            codigo_modulo=data.get('codigo_modulo'),
            imagen=data.get('imagen_post')
        )
        
        return jsonify(nuevo_post.to_dict()), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# --- 4. VER POST POR ID ---
@posts.route('/api/posts/<int:id_post>', methods=['GET'])
def ver_post_por_id_api(id_post):
    try:
        # Llamamos al servicio para buscar el post específico
        post_encontrado = PostService.obtener_por_id(id_post)
        
        # Si el servicio devuelve None (porque no existe en la BD), mandamos un 404
        if not post_encontrado:
            return jsonify({"error": f"No se encontró ningún post con el ID {id_post}"}), 404
            
        # Si existe, lo transformamos a JSON con el to_dict() que acabamos de crear
        return jsonify(post_encontrado.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# --- 5. VER POSTS POR ID DE USUARIO ---
@posts.route('/api/usuarios/<int:id_usuario>/posts', methods=['GET'])
def ver_posts_usuario_api(id_usuario):
    try:
        lista = PostService.ver_posts_por_usuario(id_usuario)
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500