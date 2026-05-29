from flask import Blueprint, jsonify, request, redirect, url_for, g, flash
from src.services.respuesta_service import RespuestaService 

respuestas = Blueprint('respuestas', __name__)

@respuestas.route('/posts/<int:id_post>/publicar', methods=['POST'])
def crear_respuesta_web(id_post):

    contenido = request.form.get('contenido_respuesta')

    usuario_actual = getattr(g, 'current_user', None)
    if not usuario_actual:
        flash("Debes iniciar sesión para publicar una respuesta.")
        return redirect(url_for('auth.login'))

    id_usuario = usuario_actual.id_usuario

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

@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['POST'])
def crear_respuesta_api(id_post):
    datos = request.get_json()
    if not datos or 'contenido_respuesta' not in datos or 'id_usuario' not in datos:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
        
    try:
        nueva = RespuestaService.crear_respuesta(
            id_post=id_post,
            id_usuario=datos['id_usuario'],
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

@respuestas.route('/api/respuestas/<int:id_respuesta>', methods=['PUT', 'DELETE'])
def gestionar_respuesta_api(id_respuesta):
    return jsonify({"mensaje": "Gestión completada"}), 200