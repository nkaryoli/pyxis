from flask import Blueprint, jsonify, render_template, request, url_for, redirect, g
from src.modules.auth.controllers import _wants_json
from src.services.auth_service import AuthService
from src.services.post_service import PostService
from src.services.respuesta_service import RespuestaService
import math

posts = Blueprint('posts', __name__, template_folder='templates')

def _extraer_datos_request():
    """Obtiene los datos de la petición como JSON o como formulario HTML."""
    datos = request.get_json(silent=True)
    if datos is None:
        datos = request.form.to_dict()
    return datos or {}

class CustomPagination:
    """Clase para emular la paginación de SQLAlchemy usando listas de servicios."""
    def __init__(self, items, page, per_page):
        self.total_items = len(items)
        self.page = max(1, page)
        self.per_page = per_page
        self.pages = math.ceil(self.total_items / per_page) or 1
        
        inicio = (self.page - 1) * per_page
        fin = inicio + per_page
        self.items = items[inicio:fin]
        
        self.has_prev = self.page > 1
        self.prev_num = self.page - 1 if self.has_prev else 1
        self.has_next = self.page < self.pages
        self.next_num = self.page + 1 if self.has_next else self.pages

    def iter_pages(self, left_edge=1, right_edge=1, left_current=1, right_current=2):
        """Recrea los saltos de números de página (ej: 1 ... 4 5 [6] 7 8 ... 12)."""
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num >= self.page - left_current and num <= self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


@posts.route('/api/posts', methods=['GET'])
def listar_todos_api():
    try:
        lista = PostService.listar_todos()
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


@posts.route('/api/posts/<int:id_post>', methods=['GET'])
def ver_post_por_id_api(id_post):
    try:
        post_encontrado = PostService.obtener_por_id(id_post)
        if not post_encontrado:
            return jsonify({"error": f"No se encontró ningún post con el ID {id_post}"}), 404
            
        return jsonify(post_encontrado.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@posts.route('/api/usuarios/<int:id_usuario>/posts', methods=['GET'])
def ver_posts_usuario_api(id_usuario):
    try:
        lista = PostService.ver_posts_por_usuario(id_usuario)
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@posts.route('/api/modulos/<string:codigo_modulo>/posts', methods=['GET'])
def ver_posts_modulo_api(codigo_modulo):
    try:
        lista = PostService.ver_posts_por_modulo(codigo_modulo)
        return jsonify([p.to_dict() for p in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@posts.route('/api/posts/<int:id_post>', methods=['PUT', 'DELETE'])
def gestionar_post_api(id_post):
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        usuario_role = request.headers.get('X-User-Role')
        
        if not usuario_id_solicitante or not usuario_role:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Id o X-User-Role."}), 401

        usuario_id_solicitante = int(usuario_id_solicitante)

        post = PostService.obtener_por_id(id_post)
        if not post:
            return jsonify({"error": f"No se encontró el post con ID {id_post}"}), 404

        es_autorizado = (usuario_role in ['ADMINISTRADOR', 'PROFESOR']) or (post.id_usuario == usuario_id_solicitante)
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
    

@posts.route('/posts', methods=['GET'])
def posts_por_modulo():
    try:
        todos_posts = PostService.listar_todos() or []

        todos_posts.sort(key=lambda p: getattr(p, 'fecha_creacion_post', 0) or getattr(p, 'id_post', 0), reverse=True)
        
        page = request.args.get('page', 1, type=int)
        pagination = CustomPagination(todos_posts, page, per_page=10)
        
        is_authenticated = True if getattr(g, 'current_user', None) else False
        
        return render_template('posts.html', posts=pagination.items, pagination=pagination, is_authenticated=is_authenticated)
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500
 
 
@posts.route('/posts/<int:id_post>', methods=['GET'])
def post_respuesta(id_post):
    try:
        post_encontrado = PostService.obtener_por_id(id_post)
        if not post_encontrado:
            return render_template('errors/404.html', mensaje='Post no encontrado'), 404
        
        respuestas_post = RespuestaService.obtener_respuestas_de_post(id_post) or []

        respuestas_post.sort(key=lambda r: getattr(r, 'fecha_respuesta', 0) or getattr(r, 'id_respuesta', 0))

        respuestas_post.sort(key=lambda r: getattr(r, 'es_mejor_respuesta', False) or getattr(r, 'es_mejor', 0) == 1, reverse=True)

        page = request.args.get('page', 1, type=int)

        pagination = CustomPagination(respuestas_post, page, per_page=5)
        
        is_authenticated = True if getattr(g, 'current_user', None) else False
        
        return render_template(
            'post_detail.html', 
            post=post_encontrado, 
            respuestas=pagination.items, 
            pagination=pagination, 
            is_authenticated=is_authenticated
        )
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


@posts.route('/posts/<int:id_post>/editar', methods=['GET', 'POST'])
@AuthService.token_required
def editar_post(id_post):
    usuario = getattr(g, 'current_user', None)
    if not usuario:
        return redirect(url_for('auth.login'))
        
    post = PostService.obtener_por_id(id_post)
    if not post:
        return render_template('errors/404.html', mensaje='Post no encontrado'), 404
        
    if post.id_usuario != usuario.id_usuario:
        return render_template('errors/error.html', error='No tienes permisos para modificar este post'), 403
        
    if request.method == 'POST':
        try:
            PostService.modificar_post(
                id_post=id_post,
                titulo=request.form.get('titulo_post'),
                contenido=request.form.get('contenido_post'),
                codigo_modulo=request.form.get('codigo_modulo', post.codigo_modulo),
                imagen=getattr(post, 'imagen_post', None)
            )
            return redirect(url_for('posts.post_respuesta', id_post=id_post))
        except Exception as e:
            return render_template('errors/error.html', error=str(e)), 500
            
    lista_modulos = PostService.obtener_todos_los_modulos()
    return render_template('question_form.html', usuario=usuario, modulos=lista_modulos, post=post, edit_mode=True)


@posts.route('/posts/<int:id_post>/borrar', methods=['POST'])
@AuthService.token_required
def borrar_post(id_post):
    usuario = getattr(g, 'current_user', None)
    if not usuario:
        return redirect(url_for('auth.login'))
        
    post = PostService.obtener_por_id(id_post)
    if not post:
        return render_template('errors/404.html', mensaje='Post no encontrado'), 404
        
    if post.id_usuario != usuario.id_usuario:
        return render_template('errors/error.html', error='No tienes permisos para eliminar este post'), 403
        
    try:
        PostService.eliminar_post(id_post)
        return redirect(url_for('posts.posts_por_modulo'))
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500


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
    
@posts.route('/posts/<int:id_post>/responder', methods=['POST'])
@AuthService.token_required
def crear_respuesta(id_post):
    """Procesa el formulario clásico de HTML para añadir una respuesta."""
    usuario = getattr(g, 'current_user', None)
    if not usuario:
        return redirect(url_for('auth.login'))
        
    contenido = request.form.get('contenido_respuesta')
    
    if not contenido or not contenido.strip():
        return redirect(url_for('posts.post_respuesta', id_post=id_post))
        
    try:
        RespuestaService.crear_respuesta(
            id_post=id_post,
            id_usuario=usuario.id_usuario,
            contenido=contenido.strip(),
            es_mejor=0,
            imagen=None
        )
        return redirect(url_for('posts.post_respuesta', id_post=id_post))
        
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500