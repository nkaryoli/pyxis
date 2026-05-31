from flask import Blueprint, render_template, jsonify, request
from src.services.modulo_service import ModuloService
import math

modulos = Blueprint('modulos', __name__, template_folder='templates')

@modulos.route('/modulos')
def listar_modulos():
    """Renderiza el muro o lista con datos de los módulos académicos."""
    try:
        modulos = ModuloService.obtener_todos_los_modulos()
        return render_template('modules.html', modulos=modulos)
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500


@modulos.route('/modulos/<string:nombre_modulo>', methods=['GET'])
def detalle_modulo(nombre_modulo):
    try:
        page = request.args.get('page', 1, type=int)
        if page < 1:
            page = 1
            
        per_page = 10  
        
        modulo, todos_los_posts = ModuloService.obtener_detalle_modulo(nombre_modulo)
        
        total_items = len(todos_los_posts)
        total_pages = math.ceil(total_items / per_page) or 1
        
        inicio = (page - 1) * per_page
        fin = inicio + per_page
        posts_paginados = todos_los_posts[inicio:fin]
        
        return render_template(
            'module_detail.html', 
            modulo=modulo, 
            posts=posts_paginados,  
            page=page,
            total_pages=total_pages
        )
    except ValueError as e:
        return render_template('errors/404.html', mensaje=str(e)), 404
    except Exception as e:
        return render_template('errors/error.html', error=str(e)), 500


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

@modulos.route('/api/modulos/<string:codigo_modulo>/alumnos', methods=['GET'])
def get_alumnos_modulo(codigo_modulo):
    """Endpoint API que devuelve los alumnos matriculados en un módulo."""
    try:
        from src.repositories.matricula_repository import MatriculaRepository
        alumnos = MatriculaRepository.get_alumnos_by_modulo(codigo_modulo)
        return jsonify([
            {
                'id_usuario': a.id_usuario,
                'username': a.username,
                'email': a.email_usuario
            }
            for a in alumnos
        ]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500