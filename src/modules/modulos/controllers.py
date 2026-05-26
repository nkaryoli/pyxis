from flask import Blueprint, render_template, jsonify, request
from src.mock_forum import get_modules, get_module_by_slug, get_posts_by_module
from src.services.modulo_service import ModuloService

modulos = Blueprint('modulos', __name__, template_folder='templates')

@modulos.route('/modulos')
def listar_modulos():
    """Renderiza el muro o lista con datos de los módulos académicos."""
    try:
        return render_template('modules.html', modulos=get_modules())
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500


@modulos.route('/modulos/<string:nombre_modulo>')
def detalle_modulo(nombre_modulo):
    """Renderiza el detalle de un módulo con sus posts simulados."""
    modulo = get_module_by_slug(nombre_modulo)
    if not modulo:
        return render_template('errors/404.html', mensaje='Módulo no encontrado'), 404

    posts = get_posts_by_module(modulo['codigo_modulo'])
    return render_template('module_detail.html', modulo=modulo, posts=posts)


@modulos.route('/api/modulos', methods=['GET'])
def get_modulos():
    """Endpoint API que devuelve todos los módulos en JSON."""
    try:
        lista_modulos = ModuloService.obtener_todos_los_modulos()
        return jsonify([
            {
                'codigo_modulo': m.codigo_modulo,
                'nombre_asignatura': m.nombre_asignatura,
                'curso_modulo': m.curso_modulo
            }
            for m in lista_modulos
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@modulos.route('/api/modulos', methods=['POST'])
def post_modulo():
    """Endpoint API para crear un nuevo módulo (Requiere rol PROFESOR o ADMINISTRADOR)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        codigo = data.get('codigo_modulo')
        nombre = data.get('nombre_asignatura')
        curso = data.get('curso_modulo')
        rol_usuario = data.get('rol_usuario_activo')

        nuevo = ModuloService.crear_nuevo_modulo(codigo, nombre, curso, rol_usuario)
        
        return jsonify({
            'codigo_modulo': nuevo.codigo_modulo,
            'nombre_asignatura': nuevo.nombre_asignatura,
            'curso_modulo': nuevo.curso_modulo
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@modulos.route('/api/modulos/<string:codigo_modulo>', methods=['PUT'])
def put_modulo(codigo_modulo):
    """Endpoint API para modificar un módulo (Requiere rol PROFESOR o ADMINISTRADOR)."""
    try:
        data = request.get_json() if request.is_json else request.form
        
        nuevo_nombre = data.get('nombre_asignatura')
        nuevo_curso = data.get('curso_modulo')
        rol_usuario = data.get('rol_usuario_activo')
        
        actualizado = ModuloService.modificar_modulo(codigo_modulo, nuevo_nombre, nuevo_curso, rol_usuario)
        
        return jsonify({
            'codigo_modulo': actualizado.codigo_modulo,
            'nombre_asignatura': actualizado.nombre_asignatura,
            'curso_modulo': actualizado.curso_modulo
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@modulos.route('/api/modulos/<string:codigo_modulo>', methods=['DELETE'])
def delete_modulo(codigo_modulo):
    """Endpoint API para eliminar un módulo (Requiere rol PROFESOR o ADMINISTRADOR)."""
    try:
        data = request.get_json() if request.is_json else request.form
        rol_usuario = data.get('rol_usuario_activo') if data else request.headers.get('X-User-Rol')
        
        ModuloService.eliminar_modulo_existente(codigo_modulo, rol_usuario)
        
        return jsonify({'message': f'Módulo {codigo_modulo} eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400