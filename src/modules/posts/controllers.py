import os
import uuid
from flask import Blueprint, jsonify, render_template, request, url_for, redirect, g
from werkzeug.utils import secure_filename
from src.modules.auth.controllers import _wants_json
from src.services.auth_service import AuthService
from src.services.post_service import PostService
from src.services.respuesta_service import RespuestaService
from src.services.usuario_service import UsuarioService
import math

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
POST_UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'uploads', 'posts')
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

def allowed_post_image(filename):
    return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

posts = Blueprint('posts', __name__, template_folder='templates')

def _extraer_datos_request():
    """Obtiene los datos de la petición como JSON o como formulario HTML."""
    datos = request.get_json(silent=True)
    if datos is None:
        datos = request.form.to_dict()
    return datos or {}


@posts.route('/api/posts', methods=['GET'])
def listar_todos_api():
    """Endpoint API para listar todos los posts."""
    try:
        lista = PostService.listar_todos()
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@posts.route('/api/posts', methods=['POST'])
def crear_post_api():
    """
    Endpoint API para crear un nuevo post.
    
    Returns:
        JSON: Detalles del post creado (201) o error (403/500).
        
    Note:
        Requiere que el usuario esté matriculado en el módulo objetivo.
    """
    try:
        data = request.get_json() 
        id_usuario = data.get('id_usuario')
        codigo_modulo = data.get('codigo_modulo')
        
        # Validar que el usuario esté matriculado en el módulo
        if codigo_modulo and not UsuarioService.esta_matriculado(id_usuario, codigo_modulo):
            return jsonify({"error": "No estás matriculado en este módulo. Solo puedes hacer posts en módulos donde estés matriculado."}), 403
        
        nuevo_post = PostService.crear_post(
            titulo=data.get('titulo_post'),
            contenido=data.get('contenido_post'),
            id_usuario=id_usuario,
            codigo_modulo=codigo_modulo,
            imagen=data.get('imagen_post')
        )
        return jsonify(nuevo_post.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@posts.route('/api/posts/<int:id_post>', methods=['GET'])
def ver_post_por_id_api(id_post):
    """Endpoint API que obtiene los detalles de un post específico."""
    try:
        post_encontrado = PostService.obtener_por_id(id_post)
        if not post_encontrado:
            return jsonify({"error": f"No se encontró ningún post con el ID {id_post}"}), 404
            
        return jsonify(post_encontrado.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@posts.route('/api/usuarios/<int:id_usuario>/posts', methods=['GET'])
def ver_posts_usuario_api(id_usuario):
    """Endpoint API que obtiene los posts de un usuario paginados."""
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
    
    
@posts.route('/api/modulos/<string:codigo_modulo>/posts', methods=['GET'])
def ver_posts_modulo_api(codigo_modulo):
    """Endpoint API que lista los posts pertenecientes a un módulo."""
    try:
        lista = PostService.ver_posts_por_modulo(codigo_modulo)
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@posts.route('/api/posts/<int:id_post>', methods=['PUT', 'DELETE'])
def gestionar_post_api(id_post):
    """
    Endpoint API unificado para modificar o eliminar un post existente.
    
    Args:
        id_post (int): ID del post.
        
    Returns:
        JSON: Objeto modificado/eliminado (200), o error (401/403/404).
        
    Note:
        Requiere las cabeceras X-User-Id y X-User-Role. Validará la propiedad del post o el rol.
    """
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        usuario_rol = request.headers.get('X-User-Role')
        
        if not usuario_id_solicitante or not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Id o X-User-Role."}), 401

        usuario_id_solicitante = int(usuario_id_solicitante)

        post = PostService.obtener_por_id(id_post)
        if not post:
            return jsonify({"error": f"No se encontró el post con ID {id_post}"}), 404

        if request.method == 'DELETE':
            es_autorizado = (usuario_rol in ['ADMINISTRADOR', 'PROFESOR']) or (post.id_usuario == usuario_id_solicitante)
            if not es_autorizado:
                return jsonify({"error": "No tienes permisos para borrar este post."}), 403
            PostService.eliminar_post(id_post)
            return jsonify({"mensaje": f"Post {id_post} eliminado con éxito"}), 200
            
        elif request.method == 'PUT':
            es_autorizado = (usuario_rol == 'ADMINISTRADOR') or (post.id_usuario == usuario_id_solicitante)
            if not es_autorizado:
                return jsonify({"error": "No tienes permisos para modificar este post."}), 403
            data = request.get_json()
            is_deleted = data.get('is_deleted')
            if is_deleted is not None:
                if isinstance(is_deleted, str):
                    is_deleted = is_deleted.lower() == 'true'
                else:
                    is_deleted = bool(is_deleted)
            post_actualizado = PostService.modificar_post(
                id_post=id_post,
                titulo=data.get('titulo_post'),
                contenido=data.get('contenido_post'),
                codigo_modulo=data.get('codigo_modulo'),
                imagen=data.get('imagen_post'),
                fecha_creacion=data.get('fecha_creacion_post'),
                is_deleted=is_deleted
            )
            return jsonify(post_actualizado.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# ==========================================
# --- RUTAS PARA VISTAS (FRONTEND HTML) ---
# ==========================================

@posts.route('/posts', methods=['GET'])
def posts_por_modulo():
    """
    Renderiza la vista principal con todos los posts paginados.
    
    Returns:
        Render: Plantilla HTML 'posts.html' con la lista de posts.
    """
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


@posts.route('/posts/<int:id_post>', methods=['GET'])
def post_respuesta(id_post):
    """
    Renderiza la vista de detalles de un post junto con sus respuestas asociadas.
    
    Args:
        id_post (int): ID del post a visualizar.
        
    Returns:
        Render: Plantilla HTML 'post_detail.html' con el post y sus respuestas.
    """
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
    """
    Renderiza la vista de posts destacados, ordenados por cantidad de respuestas.
    
    Returns:
        Render: Plantilla HTML 'destacados.html' con los posts.
    """
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
    """
    Renderiza la vista de posts recientes, ordenados por fecha de creación.
    
    Returns:
        Render: Plantilla HTML 'recientes.html' con los posts.
    """
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
    """
    Muestra el formulario y procesa la inserción de un nuevo post/pregunta.
    
    Returns:
        Render/Redirect: Muestra el formulario o redirige a la vista del post tras su creación.
        
    Note:
        Valida que el usuario tenga sesión activa y esté matriculado en el módulo.
    """
    usuario = getattr(g, 'current_user', None)
    if not usuario:
        if _wants_json():
            return jsonify({'error': 'No autenticado'}), 401
        return redirect(url_for('auth.login'))
    
    lista_modulos = UsuarioService.obtener_modulos_usuario(usuario)
    
    if request.method == 'POST':
        codigo_modulo = request.form.get('codigo_modulo')
        
        if not UsuarioService.esta_matriculado(usuario, codigo_modulo):
            return "Acceso denegado: No estás matriculado en este módulo.", 403

    if request.method == 'GET':
        return render_template('question_form.html', usuario=usuario, modulos=lista_modulos)

    try:
        titulo = request.form.get('titulo_post')
        contenido = request.form.get('contenido_post')
        modulo = request.form.get('codigo_modulo')
        imagen_url = None

        if 'imagen_post' in request.files:
            file = request.files['imagen_post']
            if file and file.filename != '':
                if not allowed_post_image(file.filename):
                    return "Extensión de imagen no permitida. Usa PNG, JPG, JPEG, GIF o WEBP.", 400

                filename = secure_filename(f"post_{usuario.id_usuario}_{uuid.uuid4().hex}{os.path.splitext(file.filename)[1].lower()}")
                os.makedirs(POST_UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(POST_UPLOAD_FOLDER, filename)
                file.save(filepath)
                imagen_url = f"/static/uploads/posts/{filename}"

        PostService.crear_post(
            titulo=titulo,
            contenido=contenido,
            id_usuario=usuario.id_usuario, 
            codigo_modulo=modulo,
            imagen=imagen_url 
        )
        
        return redirect(url_for('posts.posts_por_modulo'))

    except Exception as e:
        return f"Error al guardar en la base de datos: {str(e)}", 500
    

# Funcio 'search' de la NAVBAR

@posts.route('/search', methods=['GET'])
def buscar_posts():
    """
    Renderiza la vista de resultados de búsqueda por relevancia en posts.
    
    Returns:
        Render: Plantilla HTML 'navbar_busqueda.html' con los resultados.
    """
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
