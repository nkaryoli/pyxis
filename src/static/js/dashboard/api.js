var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
/**
 * Realiza una petición JSON al servidor y maneja errores comunes.
 *
 * @param url - Ruta del endpoint.
 * @param options - Opciones de la petición.
 * @returns La respuesta en formato JSON.
 */
function requestJson(url, options) {
    return __awaiter(this, void 0, void 0, function* () {
        var _a;
        const requestInit = {
            method: options.method,
            headers: Object.assign({ "Content-Type": "application/json" }, ((_a = options.headers) !== null && _a !== void 0 ? _a : {})),
        };
        if (options.body !== undefined) {
            requestInit.body = JSON.stringify(options.body);
        }
        const response = yield fetch(url, requestInit);
        if (!response.ok) {
            let message = `Request failed with status ${response.status}`;
            try {
                const errBody = yield response.json();
                if (errBody && errBody.error) {
                    message = errBody.error;
                }
            }
            catch (_b) { }
            throw new Error(message);
        }
        return (yield response.json());
    });
}
/**
 * Crea un nuevo módulo mediante la API.
 *
 * @param payload - Datos del módulo a crear.
 */
export function crearModulo(payload) {
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
export function actualizarModulo(codigo, payload) {
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
export function eliminarModulo(codigo, rolUsuario) {
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
export function crearUsuario(payload) {
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
export function actualizarUsuario(idUsuario, payload, usuarioIdSolicitante) {
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
export function eliminarUsuario(idUsuario) {
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
export function actualizarPost(idPost, payload, userId, userRole) {
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
export function eliminarPost(idPost, userId, userRole) {
    return requestJson(`/api/posts/${encodeURIComponent(idPost)}`, {
        method: "DELETE",
        headers: {
            "X-User-Id": userId,
            "X-User-Role": userRole,
        },
    });
}
//# sourceMappingURL=api.js.map