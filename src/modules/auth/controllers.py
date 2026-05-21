from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for

from src.services.auth_service import AuthService

auth = Blueprint('auth', __name__, template_folder='templates')

def _extraer_datos_request():
	"""Obtiene los datos de la petición como JSON o como formulario HTML."""
	datos = request.get_json(silent=True)
	if datos is None:
		datos = request.form.to_dict()
	return datos or {}

def _wants_json():
	"""Indica si la respuesta debe devolverse en formato JSON."""
	return request.is_json or 'application/json' in request.headers.get('Accept', '')

@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
	"""Muestra el formulario de registro o crea un usuario nuevo."""
	if request.method == 'GET':
		return render_template('register.html')

	datos = _extraer_datos_request()

	try:
		usuario = AuthService.registrar_usuario(datos)
		respuesta = {
			'mensaje': 'Usuario registrado con éxito',
			'usuario': {
				'id_usuario': usuario.id_usuario,
				'username': usuario.username,
				'email_usuario': usuario.email_usuario,
				'rol': usuario.rol,
			},
		}

		if _wants_json():
			return jsonify(respuesta), 201

		return redirect(url_for('auth.login'))
	except ValueError as e:
		mensaje = str(e)
		if _wants_json():
			return jsonify({'error': mensaje}), 400
		return render_template('register.html', error=mensaje), 400
	except Exception:
		if _wants_json():
			return jsonify({'error': 'Error interno del servidor'}), 500
		return render_template('register.html', error='Error interno del servidor'), 500

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
	"""Muestra el formulario de login o autentica al usuario."""
	if request.method == 'GET':
		return render_template('login.html')

	datos = _extraer_datos_request()

	try:
		resultado = AuthService.autenticar_usuario(datos)
		usuario = resultado['usuario']
		token = resultado['token']

		session.clear()
		session['auth_token'] = token
		session['user_id'] = usuario.id_usuario
		session['username'] = usuario.username
		session['rol'] = usuario.rol

		respuesta = {
			'mensaje': 'Inicio de sesión correcto',
			'token': token,
			'usuario': {
				'id_usuario': usuario.id_usuario,
				'username': usuario.username,
				'email_usuario': usuario.email_usuario,
				'rol': usuario.rol,
			},
		}

		if _wants_json():
			return jsonify(respuesta), 200

		return redirect(url_for('usuarios.ver_perfil', id_usuario=usuario.id_usuario))
	except ValueError as e:
		mensaje = str(e)
		if _wants_json():
			return jsonify({'error': mensaje}), 400
		return render_template('login.html', error=mensaje), 400
	except Exception:
		if _wants_json():
			return jsonify({'error': 'Error interno del servidor'}), 500
		return render_template('login.html', error='Error interno del servidor'), 500

@auth.route('/auth/logout', methods=['GET', 'POST'])
def logout():
	"""Cierra la sesión activa y redirige al login."""
	session.clear()

	if _wants_json():
		return jsonify({'mensaje': 'Sesión cerrada correctamente'}), 200

	return redirect(url_for('auth.login'))
