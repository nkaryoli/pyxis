from flask import Blueprint, jsonify, request
from src.services.respuesta_service import RespuestaService 
from src.services.usuario_service import UsuarioService

respuestas = Blueprint('respuestas', __name__)

# --- 1. CREAR RESPUESTA (POST) ---
@respuestas.route('/api/posts/<int:id_post>/respuestas', methods=['POST'])
def crear_respuesta_api(id_post):
    datos = request.get_json()
    
    # Validación con las nuevas columnas
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


# --- 2. GET RESPUESTAS POR ID_POST ---
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
    try:
        # Extraemos las credenciales desde las cabeceras (Headers) de Postman
        usuario_id_solicitante = request.headers.get('X-User-Id')
        usuario_rol = request.headers.get('X-User-Role') # 'ALUMNO', 'PROFESOR', 'ADMINISTRADOR'
        
        if not usuario_id_solicitante or not usuario_rol:
            return jsonify({"error": "Autenticación requerida. Falta X-User-Id o X-User-Role en los Headers."}), 401

        usuario_id_solicitante = int(usuario_id_solicitante)

        # Buscamos la respuesta primero para comprobar quién es el dueño original
        respuesta = RespuestaService.obtener_por_id(id_respuesta)
        if not respuesta:
            return jsonify({"error": f"No se encontró ninguna respuesta con el ID {id_respuesta}"}), 404

        # REGLA DE AUTORIZACIÓN: ¿Es Admin? ¿Es Profesor? ¿O es el dueño de la respuesta?
        es_autorizado = (usuario_rol in ['ADMINISTRADOR', 'PROFESOR']) or (respuesta.id_usuario == usuario_id_solicitante)
        
        if not es_autorizado:
            return jsonify({"error": "No tienes permisos para modificar o borrar esta respuesta."}), 403

        # Si pasa el filtro de seguridad, ejecutamos según el método HTTP
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