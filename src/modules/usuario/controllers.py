from flask import Blueprint, render_template, jsonify, request, g
from src.services.usuario_service import UsuarioService
from src.services.auth_service import AuthService

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')


@usuarios_bp.route('/perfil/<int:id_usuario>', methods=['GET'])
@AuthService.token_required
def ver_perfil(id_usuario):
    """Renderiza la página de perfil del usuario.

    Acceso solo para el propio usuario autenticado (o bloquear acceso si el id no coincide).
    """
    try:
        usuario_actual = getattr(g, 'current_user', None)
        if not usuario_actual or usuario_actual.id_usuario != id_usuario:
            return render_template('errors/error.html', error='Acceso denegado'), 403

        usuario = UsuarioService.obtener_usuario_por_id(id_usuario)
        if not usuario:
            return render_template('404.html', mensaje="Usuario no encontrado"), 404
        return render_template('perfil.html', usuario=usuario)
    except Exception as e:
        return render_template('error.html', error=str(e))


### Endpoints de API (Backend)

@usuarios_bp.route('/api/usuarios/<int:id_usuario>', methods=['GET'])
def get_info_usuario(id_usuario):
    """Endpoint para leer la información detallada de un usuario."""
    try:        
        usuario = UsuarioService.obtener_usuario_por_id(id_usuario)
        return jsonify({
            'id_usuario': usuario.id_usuario,
            'username': usuario.username,
            'email': usuario.email_usuario,
            'rol': usuario.rol,
            'puntos': usuario.tokens
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/api/usuarios/<int:id_usuario>', methods=['PUT'])
def modificar_usuario(id_usuario):
    """Endpoint para modificar datos de usuario según permisos."""
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        datos = request.get_json()        
        
        UsuarioService.actualizar_usuario(id_usuario, datos, usuario_id_solicitante)
        return jsonify({'mensaje': 'Actualización realizada correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 403

@usuarios_bp.route('/api/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    """Endpoint para eliminar un usuario."""
    try:
        usuario_rol = request.headers.get('X-User-Role')
        UsuarioService.eliminar_usuario(id_usuario, usuario_rol)
        return jsonify({'mensaje': f'Usuario {id_usuario} eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403

@usuarios_bp.route('/api/usuarios/<int:id_usuario>/puntos', methods=['GET'])
def consultar_puntos(id_usuario):
    """Endpoint específico para consultar tokens."""
    try:
        puntos = UsuarioService.obtener_puntos_usuario(id_usuario)
        return jsonify({'id_usuario': id_usuario, 'puntos': puntos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500