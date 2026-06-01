type HttpMethod = "POST" | "PUT" | "DELETE";

interface RequestOptions {
	method: HttpMethod;
	headers?: Record<string, string>;
	body?: unknown;
}

/**
 * Realiza una petición JSON al servidor y maneja errores comunes.
 * 
 * @param url - Ruta del endpoint.
 * @param options - Opciones de la petición.
 * @returns La respuesta en formato JSON.
 */
async function requestJson<T>(
	url: string,
	options: RequestOptions,
): Promise<T> {
	const requestInit: RequestInit = {
		method: options.method,
		headers: {
			"Content-Type": "application/json",
			...(options.headers ?? {}),
		},
	};

	if (options.body !== undefined) {
		requestInit.body = JSON.stringify(options.body);
	}

	const response = await fetch(url, requestInit);

	if (!response.ok) {
		let message = `Request failed with status ${response.status}`;
		try {
			const errBody = await response.json() as { error?: string };
			if (errBody && errBody.error) {
				message = errBody.error;
			}
		} catch {}
		throw new Error(message);
	}

	return (await response.json()) as T;
}

/**
 * Crea un nuevo módulo mediante la API.
 * 
 * @param payload - Datos del módulo a crear.
 */
export function crearModulo(payload: {
	codigo_modulo: string;
	nombre_asignatura: string;
	curso_modulo: string;
	rol_usuario_activo: string;
}): Promise<unknown> {
	return requestJson("/api/modulos", {
		method: "POST",
		body: payload,
	});
}

/**
 * Actualiza un módulo existente.
 * 
 * @param codigo - Código del módulo.
 * @param payload - Datos a actualizar.
 */
export function actualizarModulo(
	codigo: string,
	payload: {
		nombre_asignatura?: string;
		curso_modulo?: string;
		rol_usuario_activo?: string;
		is_deleted?: boolean;
	},
): Promise<unknown> {
	return requestJson(`/api/modulos/${encodeURIComponent(codigo)}`, {
		method: "PUT",
		body: payload,
	});
}

/**
 * Elimina (o desactiva) un módulo por su código.
 * 
 * @param codigo - Código del módulo a eliminar.
 * @param rolUsuario - Rol del usuario que realiza la acción.
 */
export function eliminarModulo(
	codigo: string,
	rolUsuario: string,
): Promise<unknown> {
	return requestJson(`/api/modulos/${encodeURIComponent(codigo)}`, {
		method: "DELETE",
		body: { rol_usuario_activo: rolUsuario },
	});
}

/**
 * Crea un nuevo usuario.
 * 
 * @param payload - Datos del nuevo usuario.
 */
export function crearUsuario(payload: {
	email_usuario: string;
	password_usuario: string;
	rol: string;
	modulos?: string[];
}): Promise<unknown> {
	return requestJson("/api/usuarios", {
		method: "POST",
		body: payload,
	});
}

/**
 * Actualiza los datos de un usuario existente.
 * 
 * @param idUsuario - ID del usuario objetivo.
 * @param payload - Datos a actualizar.
 * @param usuarioIdSolicitante - ID del usuario que ejecuta la acción.
 */
export function actualizarUsuario(
	idUsuario: string,
	payload: Record<string, unknown>,
	usuarioIdSolicitante: string,
): Promise<unknown> {
	return requestJson(`/api/usuarios/${encodeURIComponent(idUsuario)}`, {
		method: "PUT",
		headers: {
			"X-User-Id": usuarioIdSolicitante,
		},
		body: payload,
	});
}

/**
 * Elimina un usuario del sistema.
 * 
 * @param idUsuario - ID del usuario a eliminar.
 */
export function eliminarUsuario(idUsuario: string): Promise<unknown> {
	return requestJson(`/api/usuarios/${encodeURIComponent(idUsuario)}`, {
		method: "DELETE",
	});
}

/**
 * Actualiza la información de un post.
 * 
 * @param idPost - ID del post.
 * @param payload - Campos a modificar.
 * @param userId - ID del usuario solicitante.
 * @param userRole - Rol del usuario solicitante.
 */
export function actualizarPost(
	idPost: string,
	payload: {
		titulo_post?: string;
		contenido_post?: string;
		is_deleted?: boolean;
	},
	userId: string,
	userRole: string,
): Promise<unknown> {
	return requestJson(`/api/posts/${encodeURIComponent(idPost)}`, {
		method: "PUT",
		headers: {
			"X-User-Id": userId,
			"X-User-Role": userRole,
		},
		body: payload,
	});
}

/**
 * Elimina un post de forma lógica.
 * 
 * @param idPost - ID del post a eliminar.
 * @param userId - ID del usuario solicitante.
 * @param userRole - Rol del usuario solicitante.
 */
export function eliminarPost(
	idPost: string,
	userId: string,
	userRole: string,
): Promise<unknown> {
	return requestJson(`/api/posts/${encodeURIComponent(idPost)}`, {
		method: "DELETE",
		headers: {
			"X-User-Id": userId,
			"X-User-Role": userRole,
		},
	});
}
