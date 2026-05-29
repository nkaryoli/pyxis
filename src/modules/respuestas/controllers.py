from flask import Blueprint, jsonify, request, redirect, url_for, g, flash
from src.services.respuesta_service import RespuestaService 
from src.services.usuario_service import UsuarioService

respuestas = Blueprint('respuestas', __name__)

@respuestas.route('/posts/<int:id_post>/publicar', methods=['POST'])
def crear_respuesta_web(id_post):

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
    
    try:
        RespuestaService.crear_respuesta(
            id_post=id_post,
            id_usuario=id_usuario,
            contenido=contenido
        )
        flash("Respuesta publicada con éxito.")
    except Exception as e:
        flash(f"Error al guardar: {str(e)}")
        
    return redirect(url_for('posts.post_respuesta', id_post=id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/editar', methods=['POST'])
def editar_respuesta_web(id_respuesta):
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

    try:
        RespuestaService.modificar_respuesta(id_respuesta, contenido=contenido)
        flash("Respuesta actualizada con éxito.")
    except Exception as e:
        flash(f"Error al actualizar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/eliminar', methods=['POST'])
def eliminar_respuesta_web(id_respuesta):
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

@respuestas.route('/respuestas/<int:id_respuesta>/validar', methods=['POST'])
def validar_respuesta_web(id_respuesta):
    usuario_actual = getattr(g, 'current_user', None)
    respuesta = RespuestaService.obtener_por_id(id_respuesta)
    if not usuario_actual or not respuesta or usuario_actual.rol not in ['PROFESOR', 'ADMINISTRADOR']:
        flash("No tienes permiso para validar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post if respuesta else 0))

    try:
        RespuestaService.modificar_respuesta(id_respuesta, es_mejor=1)
        flash("Respuesta validada como Mejor Respuesta.")
    except Exception as e:
        flash(f"Error al validar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/respuestas/<int:id_respuesta>/desvalidar', methods=['POST'])
def desvalidar_respuesta_web(id_respuesta):
    usuario_actual = getattr(g, 'current_user', None)
    respuesta = RespuestaService.obtener_por_id(id_respuesta)
    if not usuario_actual or not respuesta or usuario_actual.rol not in ['PROFESOR', 'ADMINISTRADOR']:
        flash("No tienes permiso para desvalidar esta respuesta.")
        return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post if respuesta else 0))

    try:
        RespuestaService.modificar_respuesta(id_respuesta, es_mejor=0)
        flash("Respuesta desvalidada.")
    except Exception as e:
        flash(f"Error al desvalidar: {str(e)}")

    return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))

@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['POST'])
def crear_respuesta_api(id_post):
    datos = request.get_json()
    if not datos or 'contenido_respuesta' not in datos or 'id_usuario' not in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    
    try:
        from src.services.post_service import PostService
        id_usuario = datos['id_usuario']
        
        # Obtener el post para verificar su módulo
        post = PostService.obtener_por_id(id_post)
        if not post:
            return jsonify({"error": "El post no existe"}), 404
        
        # Validar que el usuario esté matriculado en el módulo del post
        if post.codigo_modulo and not UsuarioService.esta_matriculado(id_usuario, post.codigo_modulo):
            return jsonify({"error": "No estás matriculado en el módulo de este post. Solo puedes responder en posts de módulos donde estés matriculado."}), 403
        
        nueva = RespuestaService.crear_respuesta(
            id_post=id_post,
            id_usuario=id_usuario,
            contenido=datos['contenido_respuesta']
        )
        return jsonify({"mensaje": "Respuesta creada", "respuesta": nueva.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['GET'])
def listar_respuestas_post_api(id_post):
    try:
        lista = RespuestaService.obtener_respuestas_de_post(id_post)
        return jsonify([r.to_dict() for r in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- 3. GET RESPUESTAS POR ID_USUARIO ---
@respuestas.route('/api/usuarios/<int:id_usuario>/respuestas', methods=['GET'])
def ver_respuestas_usuario_api(id_usuario):
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


# --- 4. GESTIONAR RESPUESTA POR ID (PUT y DELETE con verificación de Rol y Propiedad) ---
@respuestas.route('/api/respuestas/<int:id_respuesta>', methods=['PUT', 'DELETE'])
def gestionar_respuesta_api(id_respuesta):
    return jsonify({"mensaje": "Gestión completada"}), 200