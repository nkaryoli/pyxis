from flask import Blueprint, render_template, jsonify
from src.services.prueba_service import PruebaService

pruebas = Blueprint('pruebas', __name__, template_folder='templates')

@pruebas.route('/')
def test_entorno():
    """Renderiza el muro con datos de prueba."""
    try:
        pruebas = PruebaService.obtener_todas_pruebas()
        return render_template('prueba.html', pruebas=pruebas)
    except Exception as e:
        return render_template('prueba.html', pruebas=[], error=str(e))

@pruebas.route('/api/pruebas', methods=['GET'])
def get_pruebas():
    """Endpoint API que devuelve todas las pruebas en JSON."""
    try:
        pruebas = PruebaService.obtener_todas_pruebas()
        return jsonify([
            {
                'id_prueba': p.id_prueba,
                'titulo': p.titulo,
                'descripcion': p.descripcion
            }
            for p in pruebas
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500