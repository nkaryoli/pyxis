from flask import Blueprint, jsonify, request, redirect, url_for, render_template, g
from src.services.respuesta_service import RespuestaService 
from src.services.auth_service import AuthService

respuestas = Blueprint('respuestas', __name__, template_folder='templates')

@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['POST'])
def crear_respuesta_api(id_post):
    datos = request.get_json()
    
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


@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['GET'])
def listar_respuestas_post_api(id_post):
    try:
        lista = RespuestaService.obtener_respuestas_de_post(id_post)
        return jsonify([r.to_dict() for r in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@respuestas.route('/api/usuarios/<int:id_usuario>/respuestas', methods=['GET'])
def ver_respuestas_usuario_api(id_usuario):
    try:
        lista = RespuestaService.obtener_respuestas_de_usuario(id_usuario)
        return jsonify([r.to_dict() for r in lista]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@respuestas.route('/api/respuestas/<int:id_respuesta>', methods=['PUT', 'DELETE'])
def gestionar_respuesta_api(id_respuesta):
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        usuario_rol = request.headers.get('X-User-Role') 
        
        if not usuario_id_solicitante or not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Id o X-User-Role en los Headers."}), 401

        usuario_id_solicitante = int(usuario_id_solicitante)

        respuesta = RespuestaService.obtener_por_id(id_respuesta)
        if not respuesta:
            return jsonify({"error": f"No se encontró ninguna respuesta con el ID {id_respuesta}"}), 404

        es_autorizado = (usuario_rol in ['ADMINISTRADOR', 'PROFESOR']) or (respuesta.id_usuario == usuario_id_solicitante)
        
        if not es_autorizado:
            return jsonify({"error": "No tienes permisos para modificar o borrar esta respuesta."}), 403

        if request.method == 'DELETE':
            RespuestaService.eliminar_respuesta(id_respuesta)
            return jsonify({"mensaje": f"Respuesta con ID {id_respuesta} eliminada correctamente"}), 200
            
        elif request.method == 'PUT':
            datos = request.get_json()
            respuesta_actualizada = RespuestaService.modificar_respuesta(
                id_respuesta=id_respuesta,
                contenido=datos.get('contenido_respuesta'),
                imagen=datos.get('imagen_respuesta')
            )
            return jsonify({"mensaje": "Respuesta modificada con éxito", "respuesta": respuesta_actualizada.to_dict()}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@respuestas.route('/respuestas/<int:id_respuesta>/editar', methods=['GET', 'POST'])
@AuthService.token_required
def editar_respuesta(id_respuesta):
    """Muestra el formulario de edición y actualiza la respuesta."""
    usuario = getattr(g, 'current_user', None)
    if not usuario:
        return redirect(url_for('auth.login'))
        
    try:
        respuesta = RespuestaService.obtener_por_id(id_respuesta)
        if not respuesta:
            return render_template('errors/404.html', mensaje='Respuesta no encontrada'), 404

        if respuesta.id_usuario != usuario.id_usuario:
            return render_template('errors/error.html', error='No tienes autorización para modificar contenido ajeno.'), 403
            
        if request.method == 'POST':
            nuevo_contenido = request.form.get('contenido_respuesta')
            RespuestaService.modificar_respuesta(id_respuesta, contenido=nuevo_contenido)
            return redirect(url_for('posts.post_respuesta', id_post=respuesta.id_post))
            
        return render_template('editar_respuesta.html', respuesta=respuesta, usuario=usuario)
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500


@respuestas.route('/respuestas/<int:id_respuesta>/borrar', methods=['POST'])
@AuthService.token_required
def borrar_respuesta(id_respuesta):
    """Elimina físicamente una respuesta y redirige de vuelta al post."""
    usuario = getattr(g, 'current_user', None)
    if not usuario:
        return redirect(url_for('auth.login'))
    
    try:
        respuesta = RespuestaService.obtener_por_id(id_respuesta)
        if not respuesta:
            return render_template('errors/404.html', mensaje='Respuesta no encontrada'), 404
            
        # Control estricto de seguridad en el servidor
        if respuesta.id_usuario != usuario.id_usuario:
            return render_template('errors/error.html', error='No tienes permisos para borrar esta respuesta.'), 403
            
        id_post_original = respuesta.id_post
        RespuestaService.eliminar_respuesta(id_respuesta)
        
        return redirect(url_for('posts.post_respuesta', id_post=id_post_original))
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500