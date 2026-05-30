import os
import math
from flask import Blueprint, render_template, jsonify, request, g, current_app, url_for
from werkzeug.utils import secure_filename
from src.services.usuario_service import UsuarioService
from src.services.auth_service import AuthService
from src.services.modulo_service import ModuloService
from src.services.post_service import PostService
from src.services.tokens_service import TokensService

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'uploads', 'perfiles')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@usuarios_bp.route('/perfil/<int:id_usuario>', methods=['GET'])
@AuthService.token_required
def ver_perfil(id_usuario):
    """
    Renderiza la vista HTML del perfil público de un usuario.

    Requiere autenticación. El usuario solicitante solo puede acceder a su propio perfil.

    Args:
        id_usuario (int): ID del usuario cuyo perfil se desea ver.

    Returns:
        Render: Plantilla HTML 'perfil.html' con los datos del usuario y sus posts, 
                o una vista de error (403/404) si no está autorizado o no existe.
    """
    try:
        usuario_actual = getattr(g, 'current_user', None)
        if not usuario_actual or int(usuario_actual.id_usuario) != int(id_usuario):
            return render_template('errors/error.html', error='Acceso denegado'), 403

        usuario, posts = UsuarioService.obtener_usuario_por_id(id_usuario)
        
        if not usuario:
            return render_template('404.html', mensaje="Usuario no encontrado"), 404

        return render_template('perfil.html', usuario=usuario, post=posts)
        
    except Exception as e:
        return render_template('errors/error.html', error=str(e))


@usuarios_bp.route('/dashboard', methods=['GET'])
@AuthService.token_required
def dashboard():
    """
    Renderiza la vista principal del Dashboard de control.

    Permite a los roles PROFESOR y ADMINISTRADOR supervisar las métricas de la plataforma,
    módulos, usuarios, posts, etc.

    Returns:
        Render: Plantilla HTML 'dashboard.html' con el resumen de métricas,
                listado de recursos y accesos rápidos según el rol.
    """
    usuario_actual = getattr(g, 'current_user', None)
    if not usuario_actual:
        return render_template('errors/401.html'), 401

    rol = (usuario_actual.rol or '').upper()
    if rol not in ['PROFESOR', 'ADMINISTRADOR']:
        return render_template('errors/403.html'), 403

    modulos = ModuloService.obtener_todos_los_modulos()
    from src.repositories.matricula_repository import MatriculaRepository
    for m in modulos:
        m.alumnos_count = MatriculaRepository.get_conteo_alumnos_por_modulo(m.codigo_modulo)

    usuarios = UsuarioService.obtener_todos_los_usuarios()
    posts = PostService.listar_todos()
    tokens = TokensService.obtener_todos_los_tokens()

    if rol == 'ADMINISTRADOR':
        accesos_rapidos = [
            {
                'titulo': 'Control administrativo',
                'descripcion': 'Bajar directamente al bloque de supervisión global.',
                'enlace': url_for('usuarios.dashboard') + '#control-administrativo',
            },
            {
                'titulo': 'Gestionar usuarios',
                'descripcion': 'Revisar perfiles y controlar permisos.',
                'enlace': url_for('usuarios.ver_perfil', id_usuario=usuario_actual.id_usuario),
            },
            {
                'titulo': 'Ver módulos',
                'descripcion': 'Inspeccionar el catálogo completo de módulos.',
                'enlace': url_for('modulos.listar_modulos'),
            },
        ]
    else:
        accesos_rapidos = [
            {
                'titulo': 'Gestionar módulos',
                'descripcion': 'Crear, editar y revisar módulos activos.',
                'enlace': url_for('modulos.listar_modulos'),
            },
            {
                'titulo': 'Ver posts recientes',
                'descripcion': 'Detectar preguntas activas y participar rápido.',
                'enlace': url_for('posts.destacados_page'),
            },
            {
                'titulo': 'Abrir perfil',
                'descripcion': 'Actualizar tu foto y revisar tu actividad.',
                'enlace': url_for('usuarios.ver_perfil', id_usuario=usuario_actual.id_usuario),
            },
        ]

    resumen = {
        'modulos': len(modulos),
        'posts': len(posts),
        'tokens': len(tokens),
    }

    return render_template(
        'dashboard.html',
        usuario=usuario_actual,
        rol=rol,
        resumen=resumen,
        accesos_rapidos=accesos_rapidos,
        modulos=modulos,
        todos_los_modulos=modulos,
        usuarios=usuarios,
        posts=posts,
        tokens=tokens[:6]
    )


@usuarios_bp.route('/api/usuarios', methods=['POST'])
@AuthService.token_required
def crear_usuario_api():
    """
    Endpoint de API para dar de alta un nuevo usuario en la plataforma.

    Requiere autenticación. Solo accesible para administradores.

    Returns:
        JSON: Mensaje de confirmación y datos básicos del usuario creado (201),
            o detalles del error (400/403/500).
    """
    usuario_actual = getattr(g, 'current_user', None)
    rol = (usuario_actual.rol or '').upper() if usuario_actual else ''
    if rol != 'ADMINISTRADOR':
        return jsonify({'error': 'No tienes permisos para crear usuarios'}), 403

    datos = request.get_json(silent=True) or {}
    try:
        usuario = AuthService.registrar_usuario_con_rol(datos, datos.get('rol', 'ALUMNO'))
        codigos_modulos = datos.get('modulos')
        if codigos_modulos and isinstance(codigos_modulos, list):
            from src.repositories.matricula_repository import MatriculaRepository
            from datetime import datetime, timedelta
            fecha_inicio = datetime.now()
            fecha_final = fecha_inicio + timedelta(days=365)
            for cod in codigos_modulos:
                if cod and str(cod).strip():
                    MatriculaRepository.create(
                        id_usuario=usuario.id_usuario,
                        codigo_modulo=str(cod).strip(),
                        fecha_inicio=fecha_inicio,
                        fecha_final=fecha_final
                    )
        return jsonify({
            'mensaje': 'Usuario creado correctamente',
            'usuario': {
                'id_usuario': usuario.id_usuario,
                'username': usuario.username,
                'email_usuario': usuario.email_usuario,
                'rol': usuario.rol,
                'tokens': usuario.tokens,
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@usuarios_bp.route('/api/usuarios/<int:id_usuario>', methods=['DELETE'])
@AuthService.token_required
def eliminar_usuario_api(id_usuario):
    """
    Endpoint de API para eliminar físicamente a un usuario.

    Requiere autenticación. Solo accesible para administradores.

    Args:
        id_usuario (int): ID del usuario a eliminar.

    Returns:
        JSON: Mensaje de confirmación del éxito (200), o detalles del error (400/403/404/500).
    """
    usuario_actual = getattr(g, 'current_user', None)
    rol = (usuario_actual.rol or '').upper() if usuario_actual else ''
    if rol != 'ADMINISTRADOR':
        return jsonify({'error': 'No tienes permisos para eliminar usuarios'}), 403

    try:
        eliminado = UsuarioService.eliminar_usuario(id_usuario, rol)
        if not eliminado:
            return jsonify({'error': f'No se encontró ningún usuario con el ID {id_usuario}'}), 404
        return jsonify({'mensaje': f'Usuario {id_usuario} eliminado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

### Endpoints de API (Backend)

@usuarios_bp.route('/api/usuarios/<int:id_usuario>/foto', methods=['POST'])
def subir_foto_perfil(id_usuario):
    """
    Sube y guarda la foto de perfil física de un usuario, actualizando su URL en la BD.

    Args:
        id_usuario (int): ID del usuario de destino de la imagen.

    Returns:
        JSON: Confirmación y la URL lógica asignada (200), o detalles del error (400/500).
    """
    try:
        if 'foto' not in request.files:
            return jsonify({'error': 'No se ha enviado ninguna foto'}), 400
        
        file = request.files['foto']
        if file.filename == '':
            return jsonify({'error': 'Archivo no seleccionado'}), 400

        usuario_id_solicitante = request.headers.get('X-User-Id')
        
        ext = os.path.splitext(file.filename)[1].lower()
        filename = secure_filename(f"user_{id_usuario}{ext}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        file.save(filepath)
        print(f"DEBUG: Archivo guardado en {filepath}")

        url_para_db = f"/static/uploads/perfiles/{filename}"

        UsuarioService.actualizar_usuario(id_usuario, {'imagen_usuario': url_para_db}, usuario_id_solicitante)

        return jsonify({
            'mensaje': 'Foto subida correctamente',
            'url': url_para_db
        }), 200

    except Exception as e:
        print(f"ERROR CRÍTICO SUBIDA: {str(e)}")
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/api/usuarios/<int:id_usuario>', methods=['GET'])
def get_info_usuario(id_usuario):
    """
    Endpoint de API para consultar la información pública y perfil de un usuario concreto.

    Args:
        id_usuario (int): ID del usuario a consultar.

    Returns:
        JSON: Atributos básicos (email, username, rol, tokens) del usuario (200), o error (500).
    """
    try:        
        from src.repositories.matricula_repository import MatriculaRepository
        usuario, _ = UsuarioService.obtener_usuario_por_id(id_usuario)
        matriculas = MatriculaRepository.get_by_usuario_id(id_usuario)
        return jsonify({
            'id_usuario': usuario.id_usuario,
            'username': usuario.username,
            'email': usuario.email_usuario,
            'rol': usuario.rol,
            'tokens': usuario.tokens,
            'modulos': [m.codigo_modulo for m in matriculas]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/api/usuarios/<int:id_usuario>', methods=['PUT'])
def modificar_usuario(id_usuario):
    """
    Endpoint de API para actualizar el perfil e información del usuario destino.

    Args:
        id_usuario (int): ID del usuario que se desea actualizar.

    Returns:
        JSON: Confirmación de actualización (200), o mensaje del error (403).
    """
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        datos = request.get_json()        
        UsuarioService.actualizar_usuario(id_usuario, datos, usuario_id_solicitante)
        return jsonify({'mensaje': 'Actualización realizada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403
    
    
@usuarios_bp.route('/api/usuarios/<int:id_usuario>/posts', methods=['GET'])
def get_posts_api(id_usuario):
    """
    Endpoint de API para obtener los posts creados por un usuario paginados.

    Args:
        id_usuario (int): ID del usuario creador de los posts.

    Returns:
        JSON: Lista de posts de la página e información del total de páginas (200).
    """
    page = request.args.get('page', 1, type=int)
    items, total_pages = UsuarioService.obtener_posts_paginados(id_usuario, page)
    
    return jsonify({
        'items': items,
        'total_pages': total_pages
    })
    
    
@usuarios_bp.route('/api/usuarios/<int:id_usuario>/respuestas', methods=['GET'])
def get_respuestas_api(id_usuario):
    """
    Endpoint de API para obtener de forma paginada las respuestas de un usuario.

    Args:
        id_usuario (int): ID del usuario creador de las respuestas.

    Returns:
        JSON: Listado paginado de respuestas e información de páginas totales (200).
    """
    page = request.args.get('page', 1, type=int)
    items, total_pages = UsuarioService.obtener_respuestas_paginadas(id_usuario, page)
    
    return jsonify({
        'items': items,
        'total_pages': total_pages
    })
    
    
@usuarios_bp.route('/api/usuarios/<int:id_usuario>/notificaciones', methods=['GET'])
def get_notificaciones_api(id_usuario):
    """
    Endpoint de API para obtener las notificaciones de respuestas en los posts del usuario.

    Args:
        id_usuario (int): ID del usuario propietario de los posts con notificaciones.

    Returns:
        JSON: Listado paginado de notificaciones e información de páginas totales (200).
    """
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1

    items, total_pages = UsuarioService.obtener_notificaciones_paginadas(id_usuario, page)
    return jsonify({
        'items': items,
        'total_pages': total_pages
    }), 200