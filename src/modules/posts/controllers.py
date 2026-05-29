from flask import Blueprint, jsonify, render_template, request, url_for, redirect, g
from src.modules.auth.controllers import _wants_json
from src.services.auth_service import AuthService
from src.services.post_service import PostService
from src.services.respuesta_service import RespuestaService
from src.services.usuario_service import UsuarioService
import math

posts = Blueprint('posts', __name__, template_folder='templates')

def _extraer_datos_request():
    """Obtiene los datos de la petición como JSON o como formulario HTML."""
    datos = request.get_json(silent=True)
    if datos is None:
        datos = request.form.to_dict()
    return datos or {}


# --- APIS 

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
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
        items, total_pages = UsuarioService.obtener_posts_paginados(id_usuario, page)
        return jsonify({
            'items': items,
            'total_pages': total_pages
        }), 200
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
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
        per_page = 5 
        todos_resultados = PostService.listar_todos()
        total_items = len(todos_resultados)
        total_pages = math.ceil(total_items / per_page) or 1
        
        inicio = (page - 1) * per_page
        fin = inicio + per_page
        posts_paginados = todos_resultados[inicio:fin]
        
        return render_template(
            'posts.html', 
            posts=posts_paginados, 
            page=page, 
            total_pages=total_pages, 
            query="" 
        )
        
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500
 
 
import math
from flask import render_template, request

@posts.route('/posts/<int:id_post>', methods=['GET'])
def post_respuesta(id_post):
    try:

        post_encontrado = PostService.obtener_por_id(id_post)
        if not post_encontrado:
            return render_template('errors/404.html', mensaje='Post no encontrado'), 404
        

        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
            
        per_page = 10
        
        edit_respuesta_id = request.args.get('edit_respuesta', type=int)

        todas_las_respuestas = RespuestaService.obtener_respuestas_de_post(id_post)
        
        respuestas_ordenadas = sorted(
            todas_las_respuestas,
            key=lambda r: getattr(r, 'es_mejor_respuesta', 0),
            reverse=True
        )
        
        total_items = len(respuestas_ordenadas)
        total_pages = math.ceil(total_items / per_page) or 1
        
        inicio = (page - 1) * per_page
        fin = inicio + per_page
        respuestas_paginadas = respuestas_ordenadas[inicio:fin]

        edit_respuesta = None
        if edit_respuesta_id:
            posible_edicion = RespuestaService.obtener_por_id(edit_respuesta_id)
            usuario_actual = getattr(g, 'current_user', None)
            if posible_edicion and usuario_actual and (
                posible_edicion.id_usuario == usuario_actual.id_usuario or
                usuario_actual.rol in ['PROFESOR', 'ADMINISTRADOR']
            ):
                edit_respuesta = posible_edicion
        
        return render_template(
            'post_detail.html', 
            post=post_encontrado, 
            respuestas=respuestas_paginadas, 
            page=page,
            total_pages=total_pages,
            edit_respuesta=edit_respuesta
        )
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500

 
@posts.route('/destacados', methods=['GET'])
def destacados_page():
    try:
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
        per_page = 5  

        todos_los_posts = PostService.listar_todos()

        posts_ordenados = sorted(
            todos_los_posts, 
            key=lambda p: len(RespuestaService.obtener_respuestas_de_post(p.id_post)), 
            reverse=True
        )
        top_10_destacados = posts_ordenados[:10]

        total_items = len(top_10_destacados)
        total_pages = math.ceil(total_items / per_page) or 1

        inicio = (page - 1) * per_page
        fin = inicio + per_page
        posts_paginados = top_10_destacados[inicio:fin]

        return render_template(
            'destacados.html',
            posts=posts_paginados,
            page=page,
            total_pages=total_pages,
            query="" 
        )

    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500
 
 
@posts.route('/recientes', methods=['GET'])
def recientes_page():
    try:
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
            
        per_page = 5  
        
        todos_resultados = PostService.listar_recientes()
        total_items = len(todos_resultados)
        
        total_pages = math.ceil(total_items / per_page) or 1
        
        inicio = (page - 1) * per_page
        fin = inicio + per_page
        posts_paginados = todos_resultados[inicio:fin]

        return render_template(
            'recientes.html', 
            posts=posts_paginados, 
            page=page, 
            total_pages=total_pages, 
            query="" 
        )
        
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
    


    # NAVBAR

@posts.route('/search', methods=['GET'])
def buscar_posts():
    try:
        query = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        if page is None or page < 1:
            page = 1
        per_page = 5 
        if not query:
            return render_template('navbar_busqueda.html', posts=[], query="", page=1, total_pages=1, total_items=0)
        todos_resultados = PostService.buscar_por_relevancia(query)
        total_items = len(todos_resultados)
        import math
        total_pages = math.ceil(total_items / per_page) or 1
        
        inicio = (page - 1) * per_page
        fin = inicio + per_page
        posts_paginados = todos_resultados[inicio:fin]
        
        return render_template(
            'navbar_busqueda.html', 
            posts=posts_paginados, 
            query=query, 
            page=page, 
            total_pages=total_pages,
            total_items=total_items  
        )
        
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500
