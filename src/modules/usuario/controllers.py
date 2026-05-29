import os
from flask import Blueprint, render_template, jsonify, request, g, current_app
from werkzeug.utils import secure_filename
from src.services.usuario_service import UsuarioService
from src.services.auth_service import AuthService

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

# --- CONFIGURACIÓN DE RUTA ABSOLUTA CORREGIDA ---
# Si este archivo está en src/controllers/controllers.py:
# os.path.dirname(__file__) nos da '.../src/controllers'

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Ajustamos para que busque la carpeta 'static' en la raíz (sin el 'src' intermedio)
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'static', 'uploads', 'perfiles')

# Ya que confirmaste que la carpeta existe, esta línea es opcional pero segura
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@usuarios_bp.route('/perfil/<int:id_usuario>', methods=['GET'])
@AuthService.token_required
def ver_perfil(id_usuario):
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

### Endpoints de API (Backend)

@usuarios_bp.route('/api/usuarios/<int:id_usuario>/foto', methods=['POST'])
def subir_foto_perfil(id_usuario):
    """
    Endpoint para subir la foto: guarda el archivo en el servidor 
    y actualiza la URL en la base de datos.
    """
    try:
        if 'foto' not in request.files:
            return jsonify({'error': 'No se ha enviado ninguna foto'}), 400
        
        file = request.files['foto']
        if file.filename == '':
            return jsonify({'error': 'Archivo no seleccionado'}), 400

        usuario_id_solicitante = request.headers.get('X-User-Id')
        
        # 1. Procesar el nombre del archivo
        ext = os.path.splitext(file.filename)[1].lower()
        filename = secure_filename(f"user_{id_usuario}{ext}")
        
        # 2. Ruta física real para guardar el archivo
        # Usamos la ruta absoluta construida al inicio
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # 3. Guardar archivo físicamente
        file.save(filepath)
        print(f"DEBUG: Archivo guardado en {filepath}")

        # 4. URL lógica para la base de datos
        # Flask mapea /static a src/static, así que la URL debe empezar desde /static
        url_para_db = f"/static/uploads/perfiles/{filename}"

        # 5. Actualizar base de datos mediante el servicio
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
    try:        
        usuario = UsuarioService.obtener_usuario_por_id(id_usuario)
        return jsonify({
            'id_usuario': usuario.id_usuario,
            'username': usuario.username,
            'email': usuario.email_usuario,
            'rol': usuario.rol,
            'tokens': usuario.tokens
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/api/usuarios/<int:id_usuario>', methods=['PUT'])
def modificar_usuario(id_usuario):
    try:
        usuario_id_solicitante = request.headers.get('X-User-Id')
        datos = request.get_json()        
        UsuarioService.actualizar_usuario(id_usuario, datos, usuario_id_solicitante)
        return jsonify({'mensaje': 'Actualización realizada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 403
    
    
    
@usuarios_bp.route('/api/usuarios/<int:id_usuario>/posts', methods=['GET'])
def get_posts_api(id_usuario):
    page = request.args.get('page', 1, type=int)
    # Llama al servicio que ya actualizaste
    items, total_pages = UsuarioService.obtener_posts_paginados(id_usuario, page)
    
    return jsonify({
        'items': items,
        'total_pages': total_pages
    })
    
    
@usuarios_bp.route('/api/usuarios/<int:id_usuario>/respuestas', methods=['GET'])
def get_respuestas_api(id_usuario):
    page = request.args.get('page', 1, type=int)
    # Usamos el servicio que ya tienes en UsuarioService
    items, total_pages = UsuarioService.obtener_respuestas_paginadas(id_usuario, page)
    
    return jsonify({
        'items': items,
        'total_pages': total_pages
    })
    
    
@usuarios_bp.route('/api/usuarios/<int:id_usuario>/notificaciones', methods=['GET'])
def get_notificaciones_api(id_usuario):
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1

    items, total_pages = UsuarioService.obtener_notificaciones_paginadas(id_usuario, page)
    return jsonify({
        'items': items,
        'total_pages': total_pages
    }), 200