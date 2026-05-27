from flask import Blueprint, jsonify, render_template, request, url_for, redirect, g
from src.modules.auth.controllers import _wants_json
from src.services.auth_service import AuthService
from src.services.post_service import PostService
from src.services.respuesta_service import RespuestaService
# from datetime import datetime

posts = Blueprint('posts', __name__, template_folder='templates')

def _extraer_datos_request():
    """Obtiene los datos de la petición como JSON o como formulario HTML."""
    datos = request.get_json(silent=True)
    if datos is None:
        datos = request.form.to_dict()
    return datos or {}

# ==========================================
# --- APIS (RETORNAN JSON) ---
# ==========================================

# --- 1. LISTAR TODOS ---
@posts.route('/api/posts', methods=['GET'])
def listar_todos_api():
    try:
        lista = PostService.listar_todos()
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 2. CREAR ---
@posts.route('/api/posts', methods=['POST'])
def crear_post_api():
    try:
        data = request.get_json() 
        
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


# --- 3. VER POST POR ID ---
@posts.route('/api/posts/<int:id_post>', methods=['GET'])
def ver_post_por_id_api(id_post):
    try:
        post_encontrado = PostService.obtener_por_id(id_post)
        if not post_encontrado:
            return jsonify({"error": f"No se encontró ningún post con el ID {id_post}"}), 404
            
        return jsonify(post_encontrado.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 4. VER POSTS POR ID DE USUARIO ---
@posts.route('/api/usuarios/<int:id_usuario>/posts', methods=['GET'])
def ver_posts_usuario_api(id_usuario):
    try:
        lista = PostService.ver_posts_por_usuario(id_usuario)
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# --- 5. VER POSTS POR CÓDIGO DE MÓDULO ---
@posts.route('/api/modulos/<string:codigo_modulo>/posts', methods=['GET'])
def ver_posts_modulo_api(codigo_modulo):
    try:
        lista = PostService.ver_posts_por_modulo(codigo_modulo)
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 6. MODIFICAR O ELIMINAR POR ID ---
@posts.route('/api/posts/<int:id_post>', methods=['PUT', 'DELETE'])
def gestionar_post_api(id_post):
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        usuario_rol = request.headers.get('X-User-Role')
        
        if not usuario_id_solicitante or not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Id o X-User-Role."}), 401

        usuario_id_solicitante = int(usuario_id_solicitante)

        post = PostService.obtener_por_id(id_post)
        if not post:
            return jsonify({"error": f"No se encontró el post con ID {id_post}"}), 404

        es_autorizado = (usuario_rol in ['ADMINISTRADOR', 'PROFESOR']) or (post.id_usuario == usuario_id_solicitante)
        if not es_autorizado:
            return jsonify({"error": "No tienes permisos para modificar o borrar este post."}), 403

        if request.method == 'DELETE':
            PostService.eliminar_post(id_post)
            return jsonify({"mensaje": f"Post {id_post} eliminado con éxito"}), 200
            
        elif request.method == 'PUT':
            data = request.get_json()
            post_actualizado = PostService.modificar_post(
                id_post=id_post,
                titulo=data.get('titulo_post'),
                contenido=data.get('contenido_post'),
                codigo_modulo=data.get('codigo_modulo'),
                imagen=data.get('imagen_post'),
                fecha_creacion=data.get('fecha_creacion_post')
            )
            return jsonify(post_actualizado.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# ==========================================
# --- RUTAS PARA VISTAS (FRONTEND HTML) ---
# ==========================================

@posts.route('/posts', methods=['GET'])
def posts_por_modulo():
    try:
        return render_template('posts.html', posts=PostService.listar_todos())
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500
 
 
@posts.route('/posts/<int:id_post>', methods=['GET'])
def post_respuesta(id_post):
    try:
        post_encontrado = PostService.obtener_por_id(id_post)
        if not post_encontrado:
            return render_template('errors/404.html', mensaje='Post no encontrado'), 404
        
        respuestas_post = RespuestaService.obtener_respuestas_de_post(id_post)
        return render_template('post_detail.html', post=post_encontrado, respuestas=respuestas_post)
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500

 
@posts.route('/destacados', methods=['GET'])
def destacados_page():
    try:
        return render_template('destacados.html', posts=PostService.listar_todos())
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500
 
 
@posts.route('/recientes', methods=['GET'])
def recientes_page():
    try:
        return render_template('recientes.html', posts=PostService.listar_recientes())
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500



    
@posts.route('/post/crear', methods=['GET', 'POST'])
@AuthService.token_required
def crear_post():
    """Muestra el formulario y procesa la inserción de una nueva pregunta."""
    usuario = getattr(g, 'current_user', None)
    if not usuario:
        if _wants_json():
            return jsonify({'error': 'No autenticado'}), 401
        return redirect(url_for('auth.login'))
    
    lista_modulos = PostService.obtener_todos_los_modulos()

    if request.method == 'GET':
        return render_template('question_form.html', usuario=usuario, modulos=lista_modulos)

    try:
        titulo = request.form.get('titulo_post')
        contenido = request.form.get('contenido_post')
        modulo = request.form.get('codigo_modulo')
        
        PostService.crear_post(
            titulo=titulo,
            contenido=contenido,
            id_usuario=usuario.id_usuario, 
            codigo_modulo=modulo,
            imagen=None 
        )
        
        return redirect(url_for('posts.posts_por_modulo'))

    except Exception as e:
        return f"Error al guardar en la base de datos: {str(e)}", 500