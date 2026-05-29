type HttpMethod = "POST" | "PUT" | "DELETE";

interface RequestOptions {
	method: HttpMethod;
	headers?: Record<string, string>;
	body?: unknown;
}

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

export function actualizarModulo(
	codigo: string,
	payload: {
		nombre_asignatura: string;
		curso_modulo: string;
		rol_usuario_activo: string;
	},
): Promise<unknown> {
	return requestJson(`/api/modulos/${encodeURIComponent(codigo)}`, {
		method: "PUT",
		body: payload,
	});
}

export function eliminarModulo(
	codigo: string,
	rolUsuario: string,
): Promise<unknown> {
	return requestJson(`/api/modulos/${encodeURIComponent(codigo)}`, {
		method: "DELETE",
		body: { rol_usuario_activo: rolUsuario },
	});
}

export function crearUsuario(payload: {
	email_usuario: string;
	password_usuario: string;
	rol: string;
}): Promise<unknown> {
	return requestJson("/api/usuarios", {
		method: "POST",
		body: payload,
	});
}

export function actualizarUsuario(
	idUsuario: string,
	payload: Record<string, string>,
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

export function eliminarUsuario(idUsuario: string): Promise<unknown> {
	return requestJson(`/api/usuarios/${encodeURIComponent(idUsuario)}`, {
		method: "DELETE",
	});
}

export function actualizarPost(
	idPost: string,
	payload: {
		titulo_post: string;
		contenido_post: string;
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
