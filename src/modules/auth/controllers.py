from flask import Blueprint, jsonify, make_response, redirect, render_template, request, url_for, g

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


def _crear_respuesta_con_token(payload, status_code, token):
	"""Crea una respuesta y guarda el token en una cookie HttpOnly."""
	response = make_response(payload, status_code)
	response.set_cookie(
		'auth_token',
		token,
		httponly=True,
		# secure=True,  <== ACTIVAR SOLO EN PRODUCCION
		samesite='Lax',
		max_age=60 * 60 * 24,
	)
	return response


@auth.route('/auth/me', methods=['GET'])
@AuthService.token_required
def me():
	"""Devuelve el usuario autenticado o redirige al login."""
	usuario = getattr(g, 'current_user', None)
	if not usuario:
		if _wants_json():
			return jsonify({'error': 'No autenticado'}), 401
		return redirect(url_for('auth.login'))

	respuesta = {
		'id_usuario': usuario.id_usuario,
		'username': usuario.username,
		'email_usuario': usuario.email_usuario,
		'rol': usuario.rol,
		'puntos': getattr(usuario, 'tokens', None)
	}

	if _wants_json():
		return jsonify(respuesta), 200

	# Para navegación web, redirigimos al perfil público/privado
	return redirect(url_for('usuarios.ver_perfil', id_usuario=usuario.id_usuario))

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

		respuesta = {
			'mensaje': 'Inicio de sesión correcto',
			'usuario': {
				'id_usuario': usuario.id_usuario,
				'username': usuario.username,
				'email_usuario': usuario.email_usuario,
				'rol': usuario.rol,
			},
		}

		if _wants_json():
			return _crear_respuesta_con_token(jsonify(respuesta), 200, token)

		response = redirect(url_for('usuarios.ver_perfil', id_usuario=usuario.id_usuario))
		response.set_cookie(
			'auth_token',
			token,
			httponly=True,
			# secure=True,  <== ACTIVAR SOLO EN PRODUCCION
			samesite='Lax',
			max_age=60 * 60 * 24,
		)
		return response
	except ValueError as e:
		mensaje = str(e)
		if _wants_json():
			return jsonify({'error': mensaje}), 400
		return render_template('login.html', error=mensaje), 400
	except Exception:
		if _wants_json():
			return jsonify({'error': 'Error interno del servidor'}), 500
		return render_template('login.html', error='Error interno del servidor'), 500

@auth.route('/auth/logout', methods=['POST'])
def logout():
	"""Cierra la sesión activa y redirige al login.

	Nota: se acepta solo POST para evitar CSRF desde enlaces GET. Para
	protección completa, añade un token CSRF (Flask-WTF/Flask-SeaSurf) e
	verifica el token en las peticiones.
	"""
	response = make_response(
		jsonify({'mensaje': 'Sesión cerrada correctamente'}) if _wants_json() else redirect(url_for('auth.login'))
	)
	response.delete_cookie('auth_token')

	if _wants_json():
		return response, 200

	return response
