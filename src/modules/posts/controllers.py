from flask import Blueprint, jsonify, render_template, request
from src.services.post_service import PostService
from src.services.respuesta_service import RespuestaService

posts = Blueprint('posts', __name__, template_folder='templates')

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


# --- 6. MODIFICAR O ELIMINAR POR ID (CON VERIFICACIÓN DE ROL Y PROPIEDAD) ---
@posts.route('/api/posts/<int:id_post>', methods=['PUT', 'DELETE'])
def gestionar_post_api(id_post):
    try:

        usuario_id_solicitante = request.headers.get('X-User-Id')
        usuario_rol = request.headers.get('X-User-Role') # 'ALUMNO', 'PROFESOR', 'ADMINISTRADOR'
        
        if not usuario_id_solicitante or not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Id o X-User-Role en los Headers."}), 401

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
    


# RUTAS PARA EL FRONTEND


@posts.route('/posts', methods=['GET'])
def posts_por_modulo():
    try:
        return render_template('posts.html', posts=PostService.listar_todos())
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500
 
 
@posts.route('/posts/<int:id_post>', methods=['GET'])
def post_respuesta(id_post):
    try:
        # 1. Buscamos el post original en la base de datos
        post_encontrado = PostService.obtener_por_id(id_post)
        if not post_encontrado:
            return render_template('errors/404.html', mensaje='Post no encontrado'), 404
        
        # 2. Convertimos el objeto en un diccionario plano
        post_diccionario = post_encontrado.to_dict()
        
        # 3. Mapeamos TODOS los campos nativos que usa tu HTML
        post_diccionario['titulo_post'] = post_encontrado.titulo_post
        post_diccionario['contenido_post'] = post_encontrado.contenido_post
        post_diccionario['codigo_modulo'] = post_encontrado.codigo_modulo
        post_diccionario['id_usuario'] = post_encontrado.id_usuario
        
        # 4. SOLUCIÓN AL ERROR: Inyectamos las propiedades exactas que el HTML heredó del mock
        post_diccionario['created_at'] = post_encontrado.fecha_creacion_post
        post_diccionario['autor'] = f"Usuario {post_encontrado.id_usuario}"
        
        # 5. Buscamos las respuestas reales en la base de datos
        respuestas_post = RespuestaService.obtener_respuestas_de_post(id_post)
 
        # 6. Inyectamos las respuestas en la clave que recorre el bucle del HTML
        post_diccionario['respuestas'] = respuestas_post

        # 7. Enviamos el diccionario listo a la plantilla
        return render_template('post_detail.html', post=post_diccionario)

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
    
    