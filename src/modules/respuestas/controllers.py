import os
import uuid
from flask import Blueprint, jsonify, request, redirect, url_for, g, flash
from werkzeug.utils import secure_filename
from src.services.respuesta_service import RespuestaService 
from src.services.usuario_service import UsuarioService

respuestas = Blueprint('respuestas', __name__)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RESPUESTA_UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'uploads', 'respuestas')
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

def allowed_image(filename):
    return '.' in filename and os.path.splitext(filename)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@respuestas.route('/posts/<int:id_post>/publicar', methods=['POST'])
def crear_respuesta_web(id_post):
    """
    Procesa el formulario web para publicar una nueva respuesta en un post.
    
    Args:
        id_post (int): ID del post donde se responde.
        
    Returns:
        Redirect: Recarga la vista del post (post_respuesta) tras su publicación.
        
    Note:
        Verifica la autenticación y la matriculación del usuario.
    """

    contenido = request.form.get('contenido_respuesta')

    usuario_actual = getattr(g, 'current_user', None)
    if not usuario_actual:
        flash("Debes iniciar sesión para publicar una respuesta.")
        return redirect(url_for('auth.login'))

    id_usuario = usuario_actual.id_usuario
    contenido = request.form.get('contenido_respuesta')
    # Verificar matriculación antes de crear la respuesta
    from src.services.post_service import PostService
    post = PostService.obtener_por_id(id_post)
    if post and post.codigo_modulo and not UsuarioService.esta_matriculado(usuario_actual, post.codigo_modulo):
        flash("No estás matriculado en el módulo de este post. Solo puedes responder en posts de módulos donde estés matriculado.")
        return redirect(url_for('posts.post_respuesta', id_post=id_post))

    if not contenido or contenido.strip() == "":
        flash("La respuesta no puede estar vacía.")
        return redirect(url_for('posts.post_respuesta', id_post=id_post))

    imagen_url = None
    if 'imagen_respuesta' in request.files:
        file = request.files['imagen_respuesta']
        if file and file.filename != '':
            if not allowed_image(file.filename):
                flash("Solo se permiten imágenes PNG, JPG, JPEG, GIF o WEBP.")
                return redirect(url_for('posts.post_respuesta', id_post=id_post))

            filename = secure_filename(f"respuesta_{id_post}_{id_usuario}_{uuid.uuid4().hex}{os.path.splitext(file.filename)[1].lower()}")
            os.makedirs(RESPUESTA_UPLOAD_FOLDER, exist_ok=True)
            filepath = os.path.join(RESPUESTA_UPLOAD_FOLDER, filename)
            file.save(filepath)
            imagen_url = f"/static/uploads/respuestas/{filename}"
    
    try:
        RespuestaService.crear_respuesta(
            id_post=id_post,
            id_usuario=id_usuario,
            contenido=contenido,
            imagen=imagen_url
        )
        flash("Respuesta publicada con éxito.")
    except Exception as e:
        flash(f"Error al guardar: {str(e)}")
        
    return redirect(url_for('posts.post_respuesta', id_post=id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/editar', methods=['POST'])
def editar_respuesta_web(id_respuesta):
    """
    Procesa el formulario web para editar el contenido de una respuesta existente.
    
    Args:
        id_respuesta (int): ID de la respuesta a editar.
        
    Returns:
        Redirect: Recarga la vista del post asociado.
    """
    contenido = request.form.get('contenido_respuesta')

    usuario_actual = getattr(g, 'current_user', None)
    respuesta = RespuestaService.obtener_por_id(id_respuesta)
    if not usuario_actual or not respuesta:
        flash("No tienes permiso para editar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post if respuesta else 0))

    if respuesta.id_usuario != usuario_actual.id_usuario and usuario_actual.rol not in ['PROFESOR', 'ADMINISTRADOR']:
        flash("No tienes permiso para editar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

    if not contenido or contenido.strip() == "":
        flash("La respuesta no puede estar vacía.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post, edit_respuesta=id_respuesta))

    imagen_url = None
    if 'imagen_respuesta' in request.files:
        file = request.files['imagen_respuesta']
        if file and file.filename != '':
            if not allowed_image(file.filename):
                flash("Solo se permiten imágenes PNG, JPG, JPEG, GIF o WEBP.")
                return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post, edit_respuesta=id_respuesta))

            filename = secure_filename(f"respuesta_{respuesta.id_post}_{respuesta.id_usuario}_{uuid.uuid4().hex}{os.path.splitext(file.filename)[1].lower()}")
            os.makedirs(RESPUESTA_UPLOAD_FOLDER, exist_ok=True)
            filepath = os.path.join(RESPUESTA_UPLOAD_FOLDER, filename)
            file.save(filepath)
            imagen_url = f"/static/uploads/respuestas/{filename}"

    try:
        RespuestaService.modificar_respuesta(id_respuesta, contenido=contenido, imagen=imagen_url)
        flash("Respuesta actualizada con éxito.")
    except Exception as e:
        flash(f"Error al actualizar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/eliminar', methods=['POST'])
def eliminar_respuesta_web(id_respuesta):
    """
    Procesa la solicitud web para eliminar una respuesta (borrado lógico).
    
    Args:
        id_respuesta (int): ID de la respuesta a eliminar.
        
    Returns:
        Redirect: Recarga la vista del post asociado.
    """
    usuario_actual = getattr(g, 'current_user', None)
    respuesta = RespuestaService.obtener_por_id(id_respuesta)
    if not usuario_actual or not respuesta:
        flash("No tienes permiso para eliminar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post if respuesta else 0))

    if respuesta.id_usuario != usuario_actual.id_usuario and usuario_actual.rol not in ['PROFESOR', 'ADMINISTRADOR']:
        flash("No tienes permiso para eliminar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

    try:
        RespuestaService.eliminar_respuesta(id_respuesta)
        flash("Respuesta eliminada correctamente.")
    except Exception as e:
        flash(f"Error al eliminar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/restaurar', methods=['POST'])
def restaurar_respuesta_web(id_respuesta):
    """
    Procesa la solicitud web para restaurar una respuesta eliminada lógicamente.
    
    Args:
        id_respuesta (int): ID de la respuesta a restaurar.
        
    Returns:
        Redirect: Recarga la vista del post asociado.
    """
    usuario_actual = getattr(g, 'current_user', None)
    respuesta = RespuestaService.obtener_por_id(id_respuesta)
    if not usuario_actual or not respuesta:
        flash("No tienes permiso para restaurar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post if respuesta else 0))

    if usuario_actual.rol not in ['PROFESOR', 'ADMINISTRADOR']:
        flash("No tienes permiso para restaurar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

    try:
        RespuestaService.modificar_respuesta(id_respuesta, is_deleted=False)
        flash("Respuesta restaurada correctamente.")
    except Exception as e:
        flash(f"Error al restaurar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/validar', methods=['POST'])
def validar_respuesta_web(id_respuesta):
    """
    Marca una respuesta como 'Mejor Respuesta' (es_mejor=1).
    
    Args:
        id_respuesta (int): ID de la respuesta a validar.
        
    Returns:
        Redirect: Recarga la vista del post asociado.
    """
    usuario_actual = getattr(g, 'current_user', None)
    respuesta = RespuestaService.obtener_por_id(id_respuesta)
    if not usuario_actual or not respuesta or usuario_actual.rol not in ['PROFESOR', 'ADMINISTRADOR']:
        flash("No tienes permiso para validar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post if respuesta else 0))

    if respuesta.is_deleted:
        flash("No se puede validar una respuesta inactiva o eliminada.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

    try:
        RespuestaService.modificar_respuesta(id_respuesta, es_mejor=1)
        flash("Respuesta validada como Mejor Respuesta.")
    except Exception as e:
        flash(f"Error al validar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/desvalidar', methods=['POST'])
def desvalidar_respuesta_web(id_respuesta):
    """
    Desmarca una respuesta como 'Mejor Respuesta' (es_mejor=0).
    
    Args:
        id_respuesta (int): ID de la respuesta a desvalidar.
        
    Returns:
        Redirect: Recarga la vista del post asociado.
    """
    usuario_actual = getattr(g, 'current_user', None)
    respuesta = RespuestaService.obtener_por_id(id_respuesta)
    if not usuario_actual or not respuesta or usuario_actual.rol not in ['PROFESOR', 'ADMINISTRADOR']:
        flash("No tienes permiso para desvalidar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post if respuesta else 0))

    if respuesta.is_deleted:
        flash("No se puede invalidar una respuesta inactiva o eliminada.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

    try:
        RespuestaService.modificar_respuesta(id_respuesta, es_mejor=0)
        flash("Respuesta desvalidada.")
    except Exception as e:
        flash(f"Error al desvalidar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['POST'])
def crear_respuesta_api(id_post):
    """
    Endpoint API para crear una nueva respuesta.
    
    Args:
        id_post (int): ID del post al que se responde.
        
    Returns:
        JSON: Mensaje de confirmación y datos de la respuesta creada (201).
    """
    datos = request.get_json()
    if not datos or 'contenido_respuesta' not in datos or 'id_usuario' not in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    try:
        from src.services.post_service import PostService
        id_usuario = datos['id_usuario']

        post = PostService.obtener_por_id(id_post)
        try:
            from src.services.usuario_service import UsuarioService
            usuario_res = UsuarioService.obtener_usuario_por_id(id_usuario)
            usuario_obj = usuario_res[0] if isinstance(usuario_res, tuple) else usuario_res
            if not usuario_obj:
                return jsonify({"error": "El usuario no existe"}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

        if not post:
            return jsonify({"error": "El post no existe"}), 404
        
        # Validar que el usuario esté matriculado en el módulo del post
        if post.codigo_modulo and not UsuarioService.esta_matriculado(usuario_obj, post.codigo_modulo):
            return jsonify({"error": "No estás matriculado en el módulo de este post. Solo puedes responder en posts de módulos donde estés matriculado."}), 403
        
        nueva = RespuestaService.crear_respuesta(
            id_post=id_post,
            id_usuario=id_usuario,
            contenido=datos['contenido_respuesta']
        )
        return jsonify({"mensaje": "Respuesta creada con éxito", "respuesta": nueva.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['GET'])
def listar_respuestas_post_api(id_post):
    """Endpoint API que obtiene la lista de respuestas de un post."""
    try:
        lista = RespuestaService.obtener_respuestas_de_post(id_post)
        return jsonify([r.to_dict() for r in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@respuestas.route('/api/usuarios/<int:id_usuario>/respuestas', methods=['GET'])
def ver_respuestas_usuario_api(id_usuario):
    """Endpoint API que obtiene las respuestas creadas por un usuario paginadas."""
    try:
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
        items, total_pages = UsuarioService.obtener_respuestas_paginadas(id_usuario, page)
        return jsonify({
            'items': items,
            'total_pages': total_pages
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@respuestas.route('/api/respuestas/<int:id_respuesta>', methods=['PUT', 'DELETE'])
def gestionar_respuesta_api(id_respuesta):
    """
    Endpoint API unificado para modificar o eliminar una respuesta por su ID.
    
    Args:
        id_respuesta (int): ID de la respuesta objetivo.
        
    Returns:
        JSON: Detalles actualizados o mensaje de eliminación (200), o error (401/403/404).
        
    Note:
        Valida que el usuario solicitante (X-User-Id) sea el propietario o tenga rol apropiado.
    """
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        usuario_rol = request.headers.get('X-User-Role')
        
        if not usuario_id_solicitante or not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Id o X-User-Role."}), 401

        usuario_id_solicitante = int(usuario_id_solicitante)

        respuesta = RespuestaService.obtener_por_id(id_respuesta)
        if not respuesta:
            return jsonify({"error": f"No se encontró ninguna respuesta con el ID {id_respuesta}"}), 404

        if request.method == 'DELETE':
            es_autorizado = (usuario_rol in ['ADMINISTRADOR', 'PROFESOR']) or (respuesta.id_usuario == usuario_id_solicitante)
            if not es_autorizado:
                return jsonify({"error": "No tienes permisos para borrar esta respuesta."}), 403
            
            RespuestaService.eliminar_respuesta(id_respuesta)
            return jsonify({"mensaje": f"Respuesta con ID {id_respuesta} eliminada correctamente"}), 200

        elif request.method == 'PUT':
            es_autorizado = (usuario_rol == 'ADMINISTRADOR') or (respuesta.id_usuario == usuario_id_solicitante)
            if not es_autorizado:
                return jsonify({"error": "No tienes permisos para modificar esta respuesta."}), 403
            
            datos = request.get_json() or {}
            is_deleted = datos.get('is_deleted')
            if is_deleted is not None:
                if isinstance(is_deleted, str):
                    is_deleted = is_deleted.lower() == 'true'
                else:
                    is_deleted = bool(is_deleted)

            respuesta_actualizada = RespuestaService.modificar_respuesta(
                id_respuesta=id_respuesta,
                contenido=datos.get('contenido_respuesta'),
                imagen=datos.get('imagen_respuesta'),
                es_mejor=datos.get('es_mejor'),
                is_deleted=is_deleted
            )
            return jsonify({
                "mensaje": "Respuesta modificada con éxito",
                "respuesta": respuesta_actualizada.to_dict()
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500