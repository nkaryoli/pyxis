var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const ITEMS_PER_PAGE = 5;
let notificacionesLeidas = new Set();
let modulosMap = new Map();
function cargarModulos() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch('/api/modulos');
            const modulos = yield response.json();
            modulos.forEach((m) => {
                modulosMap.set(m.codigo_modulo, m.nombre_asignatura);
            });
        }
        catch (error) {
            console.error("Error al cargar módulos:", error);
        }
    });
}
function getNombreModulo(codigo) {
    return modulosMap.get(codigo) || codigo || 'General';
}
function formatearFecha(fecha) {
    try {
        // Intenta parsear la fecha en diferentes formatos
        let date;
        // Primer intento: formato ISO con T (2026-05-28T10:15:30)
        date = new Date(fecha);
        // Si falla, intenta reemplazar espacio con T (2026-05-28 10:15:30 -> 2026-05-28T10:15:30)
        if (isNaN(date.getTime()) && fecha.includes(' ')) {
            date = new Date(fecha.replace(' ', 'T'));
        }
        // Si aún falla, intenta parsear como DD/MM/YYYY o similar
        if (isNaN(date.getTime())) {
            console.warn("Fecha fallida:", fecha);
            // Intenta formato con "/" o "-"
            const parts = fecha.match(/(\d{1,4})[\/\-](\d{1,2})[\/\-](\d{1,4})/);
            if (parts && parts.length >= 4) {
                let year = parseInt(parts[1] || '2026');
                let month = parseInt(parts[2] || '1');
                let day = parseInt(parts[3] || '1');
                // Si year es pequeño, asumir que es el tercer elemento
                if (year < 100) {
                    [day, month, year] = [year, month, day];
                }
                if (day > 31) {
                    [year, month, day] = [day, month, year];
                }
                date = new Date(year, month - 1, day);
            }
        }
        // Si aún es inválida, retorna un placeholder
        if (isNaN(date.getTime())) {
            return 'Fecha no disponible';
        }
        return date.toLocaleDateString('es-ES', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    }
    catch (error) {
        return 'Fecha no disponible';
    }
}
// Ordena los items más recientes primero
function ordenarItems(items) {
    return [...items].sort((a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime());
}
function renderizarItems(items, containerSelector) {
    const contenedor = document.getElementById(containerSelector);
    if (!contenedor)
        return;
    contenedor.innerHTML = '';
    if (items.length === 0) {
        contenedor.innerHTML = `
            <div class="text-center py-10 border border-dashed border-zinc-800 rounded-xl">
                <p class="text-zinc-500">Aún no hay elementos publicados.</p>
            </div>`;
        return;
    }
    // Iteramos directamente sobre todos los items sin slice
    items.forEach((item) => {
        const isPost = item.type === 'post';
        const href = isPost ? `/posts/${item.id}` : `/posts/${item.id_post}`;
        const titulo = isPost ? item.titulo : item.titulo;
        const modulo = isPost ? (item.modulo || '') : (item.modulo || '');
        const nombreModulo = getNombreModulo(modulo);
        const moduloHTML = modulo ? `<p class="text-xs uppercase tracking-[0.3em] text-cyan-400">${nombreModulo}</p>` : '';
        const respuestasCount = isPost ? (item.respuestas_count || 0) : '';
        const respuestasHTML = respuestasCount !== '' ? `<span>${respuestasCount} respuestas</span>` : '';
        contenedor.innerHTML += `
            <a href="${href}" class="block rounded-lg border border-zinc-800 bg-zinc-900/80 p-5 transition hover:-translate-y-1 hover:border-cyan-500">
                <div class="flex flex-col lg:flex-row items-start lg:items-start justify-between gap-4">
                    <div class="flex-1 min-w-0">
                        ${moduloHTML}
                        <h3 class="mt-2 text-lg font-semibold text-white group-hover:text-cyan-300 wrap-break-word">${titulo}</h3>
                    </div>
                </div>
                <p class="mt-3 text-sm text-zinc-400 line-clamp-2">${item.contenido}</p>
                <div class="mt-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                    <div class="flex flex-wrap items-center gap-3 text-xs text-zinc-500">
                        <span>${item.autor || 'Usuario'}</span>
                        <span>·</span>
                        <span>${formatearFecha(item.fecha)}</span>
                        ${respuestasHTML ? `<span>·</span><span>${respuestasHTML}</span>` : ''}
                    </div>                    
                </div>
            </a>`;
    });
}
function renderizarNotificaciones(items, containerSelector) {
    const contenedor = document.getElementById(containerSelector);
    if (!contenedor)
        return;
    contenedor.innerHTML = '';
    const notificacionesArray = items.filter(i => i.type === 'respuesta');
    if (notificacionesArray.length === 0) {
        contenedor.innerHTML = `<div class="text-center py-10 border border-dashed border-zinc-800 rounded-xl"><p class="text-zinc-500">No hay notificaciones.</p></div>`;
        return;
    }
    notificacionesArray.forEach((notif) => {
        const leida = notificacionesLeidas.has(notif.id);
        const badgeClass = !leida ? 'bg-cyan-500/20 border-cyan-500/50' : 'bg-zinc-800/50 border-zinc-700/50';
        contenedor.innerHTML += `
            <div class="rounded-lg border ${badgeClass} bg-zinc-900/80 p-5 transition hover:border-cyan-500">
                <a href="/posts/${notif.id_post}" onclick="marcarNotificacionLeida(${notif.id}); removerNotificacion(${notif.id})" class="block">
                    <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                        <div class="flex-1">
                            <p class="text-xs uppercase tracking-[0.3em] text-cyan-400">Respuesta a tu post</p>
                            <h3 class="mt-2 text-lg font-semibold text-white">${notif.titulo}</h3>
                        </div>
                        <span class="rounded-full ${!leida ? 'bg-cyan-500/30 text-cyan-300' : 'bg-zinc-700/50 text-zinc-400'} px-3 py-1 text-xs font-medium whitespace-nowrap">${!leida ? 'Nueva' : 'Leída'}</span>
                    </div>
                    <p class="mt-3 text-sm text-zinc-400 line-clamp-2">${notif.contenido}</p>
                    <div class="mt-4 flex flex-wrap items-center gap-3 text-xs text-zinc-500">
                        <span>${notif.usuario_respondedor || 'Usuario'}</span>
                        <span></span>
                        <span>${formatearFecha(notif.fecha)}</span>
                    </div>
                </a>
            </div>`;
    });
    window.removerNotificacion = function (id) {
        var _a;
        const element = (_a = document.querySelector(`[onclick*="removerNotificacion(${id})"]`)) === null || _a === void 0 ? void 0 : _a.parentElement;
        element === null || element === void 0 ? void 0 : element.remove();
    };
}
export function cargarActividad(idUsuario) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            yield cargarModulos();
            const [postsRes, respRes, userRes] = yield Promise.all([
                fetch(`/api/usuarios/${idUsuario}/posts`).then(r => r.json()),
                fetch(`/api/usuarios/${idUsuario}/respuestas`).then(r => r.json()),
                fetch('/auth/me', { headers: { 'Accept': 'application/json' } }).then(r => r.json())
            ]);
            const postsItems = postsRes.map((p) => {
                // Ahora podemos ejecutar código antes del return
                console.log("Post recibido de la API:", p);
                return {
                    type: 'post',
                    id: p.id_post,
                    titulo: p.titulo_post,
                    contenido: p.contenido_post,
                    fecha: p.fecha_creacion || p.fecha_creacion_post || p.created_at,
                    modulo: p.codigo_modulo,
                    autor: userRes.username,
                    respuestas_count: 0
                };
            });
            for (const item of postsItems) {
                const r = yield fetch(`/api/posts/${item.id}/respuestas`).then(res => res.json());
                item.respuestas_count = r.length;
            }
            const respuestasItems = [];
            for (const r of respRes) {
                const post = yield fetch(`/api/posts/${r.id_post}`).then(res => res.json());
                respuestasItems.push({
                    type: 'respuesta', id: r.id_respuesta, titulo: post.titulo_post, contenido: r.contenido_respuesta,
                    fecha: r.fecha_respuesta, id_post: r.id_post, autor: userRes.username,
                    modulo: post.codigo_modulo
                });
            }
            const notifs = [];
            for (const post of postsRes) {
                const resps = yield fetch(`/api/posts/${post.id_post}/respuestas`).then(r => r.json());
                for (const r of resps) {
                    if (r.id_usuario !== idUsuario) {
                        notifs.push({
                            type: 'respuesta', id: r.id_respuesta, titulo: post.titulo_post,
                            contenido: r.contenido_respuesta, fecha: r.fecha_respuesta,
                            id_post: post.id_post, usuario_respondedor: r.username_autor
                        });
                    }
                }
            }
            renderizarNotificaciones(notifs, 'content-destacados');
            renderizarItems(postsItems, 'content-posts');
            renderizarItems(respuestasItems, 'content-respuestas');
        }
        catch (e) {
            console.error(e);
            ['content-destacados', 'content-posts', 'content-respuestas'].forEach(s => {
                const c = document.getElementById(s);
                if (c)
                    c.innerHTML = '<p class="text-red-500 text-center py-10">Error al cargar.</p>';
            });
        }
    });
}
function getNombreModulo(codigo) {
    return modulosMap.get(codigo) || codigo || 'General';
}
function formatearFecha(fecha) {
    try {
        // Intenta parsear la fecha en diferentes formatos
        let date;
        // Primer intento: formato ISO con T (2026-05-28T10:15:30)
        date = new Date(fecha);
        // Si falla, intenta reemplazar espacio con T (2026-05-28 10:15:30 -> 2026-05-28T10:15:30)
        if (isNaN(date.getTime()) && fecha.includes(' ')) {
            date = new Date(fecha.replace(' ', 'T'));
        }
        // Si aún falla, intenta parsear como DD/MM/YYYY o similar
        if (isNaN(date.getTime())) {
            console.warn("Fecha fallida:", fecha);
            // Intenta formato con "/" o "-"
            const parts = fecha.match(/(\d{1,4})[\/\-](\d{1,2})[\/\-](\d{1,4})/);
            if (parts && parts.length >= 4) {
                let year = parseInt(parts[1] || '2026');
                let month = parseInt(parts[2] || '1');
                let day = parseInt(parts[3] || '1');
                // Si year es pequeño, asumir que es el tercer elemento
                if (year < 100) {
                    [day, month, year] = [year, month, day];
                }
                if (day > 31) {
                    [year, month, day] = [day, month, year];
                }
                date = new Date(year, month - 1, day);
            }
        }
        // Si aún es inválida, retorna un placeholder
        if (isNaN(date.getTime())) {
            return 'Fecha no disponible';
        }
        return date.toLocaleDateString('es-ES', {
            day: '2-digit', month: '2-digit', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    }
    catch (error) {
        return 'Fecha no disponible';
    }
}
// Ordena los items más recientes primero
function ordenarItems(items) {
    return [...items].sort((a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime());
}
function renderizarItems(items, containerSelector) {
    const contenedor = document.getElementById(containerSelector);
    if (!contenedor)
        return;
    contenedor.innerHTML = '';
    if (items.length === 0) {
        contenedor.innerHTML = `
            <div class="text-center py-10 border border-dashed border-zinc-800 rounded-xl">
                <p class="text-zinc-500">Aún no hay elementos publicados.</p>
            </div>`;
        return;
    }
    // Iteramos directamente sobre todos los items sin slice
    items.forEach((item) => {
        const isPost = item.type === 'post';
        const href = isPost ? `/posts/${item.id}` : `/posts/${item.id_post}`;
        const titulo = isPost ? item.titulo : item.titulo;
        const modulo = isPost ? (item.modulo || '') : (item.modulo || '');
        const nombreModulo = getNombreModulo(modulo);
        const moduloHTML = modulo ? `<p class="text-xs uppercase tracking-[0.3em] text-cyan-400">${nombreModulo}</p>` : '';
        const respuestasCount = isPost ? (item.respuestas_count || 0) : '';
        const respuestasHTML = respuestasCount !== '' ? `<span>${respuestasCount} respuestas</span>` : '';
        contenedor.innerHTML += `
            <a href="${href}" class="block rounded-lg border border-zinc-800 bg-zinc-900/80 p-5 transition hover:-translate-y-1 hover:border-cyan-500">
                <div class="flex flex-col lg:flex-row items-start lg:items-start justify-between gap-4">
                    <div class="flex-1 min-w-0">
                        ${moduloHTML}
                        <h3 class="mt-2 text-lg font-semibold text-white group-hover:text-cyan-300 wrap-break-word">${titulo}</h3>
                    </div>
                </div>
                <p class="mt-3 text-sm text-zinc-400 line-clamp-2">${item.contenido}</p>
                <div class="mt-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                    <div class="flex flex-wrap items-center gap-3 text-xs text-zinc-500">
                        <span>${item.autor || 'Usuario'}</span>
                        <span>·</span>
                        <span>${formatearFecha(item.fecha)}</span>
                        ${respuestasHTML ? `<span>·</span><span>${respuestasHTML}</span>` : ''}
                    </div>                    
                </div>
            </a>`;
    });
}
function renderizarNotificaciones(items, containerSelector) {
    const contenedor = document.getElementById(containerSelector);
    if (!contenedor)
        return;
    contenedor.innerHTML = '';
    const normalizedNotifications = items.map((i) => {
        var _a;
        return (Object.assign(Object.assign({}, i), { type: i.type || 'respuesta', id: (_a = i.id) !== null && _a !== void 0 ? _a : i.id_respuesta, titulo: i.titulo || i.titulo_post || i.contenido_respuesta || i.contenido || 'Notificación', contenido: i.contenido || i.contenido_respuesta || '', fecha: i.fecha || i.fecha_respuesta || '', usuario_respondedor: i.usuario_respondedor || i.username_autor || i.autor || 'Usuario' }));
    });
    const notificacionesArray = normalizedNotifications.filter(i => i.type === 'respuesta');
    if (notificacionesArray.length === 0) {
        contenedor.innerHTML = `<div class="text-center py-10 border border-dashed border-zinc-800 rounded-xl"><p class="text-zinc-500">No hay notificaciones.</p></div>`;
        return;
    }
    notificacionesArray.forEach((notif) => {
        const leida = notificacionesLeidas.has(notif.id);
        const badgeClass = !leida ? 'bg-cyan-500/20 border-cyan-500/50' : 'bg-zinc-800/50 border-zinc-700/50';
        contenedor.innerHTML += `
            <div class="rounded-lg border ${badgeClass} bg-zinc-900/80 p-5 transition hover:border-cyan-500">
                <a href="/posts/${notif.id_post}" onclick="marcarNotificacionLeida(${notif.id}); removerNotificacion(${notif.id})" class="block">
                    <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                        <div class="flex-1">
                            <p class="text-xs uppercase tracking-[0.3em] text-cyan-400">Respuesta a tu post</p>
                            <h3 class="mt-2 text-lg font-semibold text-white">${notif.titulo}</h3>
                        </div>
                        <span class="rounded-full ${!leida ? 'bg-cyan-500/30 text-cyan-300' : 'bg-zinc-700/50 text-zinc-400'} px-3 py-1 text-xs font-medium whitespace-nowrap">${!leida ? 'Nueva' : 'Leída'}</span>
                    </div>
                    <p class="mt-3 text-sm text-zinc-400 line-clamp-2">${notif.contenido}</p>
                    <div class="mt-4 flex flex-wrap items-center gap-3 text-xs text-zinc-500">
                        <span>${notif.usuario_respondedor || 'Usuario'}</span>
                        <span></span>
                        <span>${formatearFecha(notif.fecha)}</span>
                    </div>
                </a>
            </div>`;
    });
    window.removerNotificacion = function (id) {
        var _a;
        const element = (_a = document.querySelector(`[onclick*="removerNotificacion(${id})"]`)) === null || _a === void 0 ? void 0 : _a.parentElement;
        element === null || element === void 0 ? void 0 : element.remove();
    };
}
export function cargarActividad(idUsuario_1) {
    return __awaiter(this, arguments, void 0, function* (idUsuario, page = 1) {
        try {
            yield cargarModulos();
            const [postsData, respData, notifData, userRes] = yield Promise.all([
                fetch(`/api/usuarios/${idUsuario}/posts?page=${page}`).then(r => r.json()),
                fetch(`/api/usuarios/${idUsuario}/respuestas?page=${page}`).then(r => r.json()),
                fetch(`/api/usuarios/${idUsuario}/notificaciones?page=${page}`).then(r => r.json()),
                fetch('/auth/me', { headers: { 'Accept': 'application/json' } }).then(r => r.json())
            ]);
            const postsArray = Array.isArray(postsData) ? postsData : postsData.items || [];
            const respArray = Array.isArray(respData) ? respData : respData.items || [];
            const notifArray = Array.isArray(notifData) ? notifData : notifData.items || [];
            const postsTotal = Array.isArray(postsData) ? 1 : (postsData.total_pages || 1);
            const respTotal = Array.isArray(respData) ? 1 : (respData.total_pages || 1);
            const notifTotal = Array.isArray(notifData) ? 1 : (notifData.total_pages || 1);
            const postsItems = postsArray.map((p) => ({
                type: 'post', id: p.id_post, titulo: p.titulo_post || p.titulo || 'Post', contenido: p.contenido_post,
                fecha: p.fecha_creacion || p.fecha_creacion_post || p.created_at,
                modulo: p.codigo_modulo, autor: userRes.username, respuestas_count: p.respuestas_count || 0
            }));
            const respuestasItems = respArray.map((r) => ({
                type: 'respuesta', id: r.id_respuesta, titulo: r.titulo_post || r.contenido_respuesta || 'Respuesta',
                contenido: r.contenido_respuesta, fecha: r.fecha_respuesta, id_post: r.id_post,
                autor: userRes.username, modulo: r.codigo_modulo
            }));
            const notifItems = notifArray.map((n) => {
                var _a;
                return ({
                    type: 'respuesta',
                    id: (_a = n.id) !== null && _a !== void 0 ? _a : n.id_respuesta,
                    titulo: n.titulo || n.titulo_post || 'Respuesta',
                    contenido: n.contenido || n.contenido_respuesta || '',
                    fecha: n.fecha || n.fecha_respuesta || '',
                    id_post: n.id_post,
                    autor: n.usuario_respondedor || n.username_autor || userRes.username,
                    modulo: n.codigo_modulo
                });
            });
            renderizarItems(postsItems, 'content-posts');
            renderizarPaginador('content-posts', page, postsTotal, idUsuario);
            renderizarItems(respuestasItems, 'content-respuestas');
            renderizarPaginador('content-respuestas', page, respTotal, idUsuario);
            renderizarNotificaciones(notifItems, 'content-destacados');
            renderizarPaginador('content-destacados', page, notifTotal, idUsuario);
        }
        catch (e) {
            console.error("Error al cargar actividad:", e);
            ['content-destacados', 'content-posts', 'content-respuestas'].forEach(s => {
                const c = document.getElementById(s);
                if (c)
                    c.innerHTML = '<p class="text-red-500 text-center py-10">Error al cargar.</p>';
            });
        }
    });
}
export function cargarDatos(containerId, page, idUsuario) {
    return __awaiter(this, void 0, void 0, function* () {
        const contenedor = document.getElementById(containerId);
        if (contenedor)
            contenedor.innerHTML = '<div class="text-center p-4">Cargando...</div>';
        try {
            let endpoint = '';
            if (containerId === 'content-posts')
                endpoint = `/api/usuarios/${idUsuario}/posts?page=${page}`;
            else if (containerId === 'content-respuestas')
                endpoint = `/api/usuarios/${idUsuario}/respuestas?page=${page}`;
            else if (containerId === 'content-destacados')
                endpoint = `/api/usuarios/${idUsuario}/notificaciones?page=${page}`;
            const response = yield fetch(endpoint);
            const data = yield response.json();
            const itemsArray = Array.isArray(data) ? data : data.items || [];
            const totalPages = Array.isArray(data) ? 1 : (data.total_pages || 1);
            let itemsRender = [];
            if (containerId === 'content-posts') {
                itemsRender = itemsArray.map((p) => ({
                    type: 'post', id: p.id_post, titulo: p.titulo_post || p.titulo || 'Post', contenido: p.contenido_post,
                    fecha: p.fecha_creacion || p.fecha_creacion_post || p.created_at,
                    modulo: p.codigo_modulo, respuestas_count: p.respuestas_count || 0
                }));
                renderizarItems(itemsRender, containerId);
            }
            else if (containerId === 'content-respuestas') {
                itemsRender = itemsArray.map((r) => ({
                    type: 'respuesta', id: r.id_respuesta, titulo: r.titulo_post || r.contenido_respuesta || 'Respuesta',
                    contenido: r.contenido_respuesta, fecha: r.fecha_respuesta, id_post: r.id_post, modulo: r.codigo_modulo
                }));
                renderizarItems(itemsRender, containerId);
            }
            else {
                const notifItems = itemsArray.map((n) => {
                    var _a;
                    return ({
                        type: 'respuesta',
                        id: (_a = n.id) !== null && _a !== void 0 ? _a : n.id_respuesta,
                        titulo: n.titulo || n.titulo_post || 'Respuesta',
                        contenido: n.contenido || n.contenido_respuesta || '',
                        fecha: n.fecha || n.fecha_respuesta || '',
                        id_post: n.id_post,
                        autor: n.usuario_respondedor || n.username_autor || 'Usuario',
                        modulo: n.codigo_modulo
                    });
                });
                renderizarNotificaciones(notifItems, containerId);
            }
            renderizarPaginador(containerId, page, totalPages, idUsuario);
        }
        catch (error) {
            console.error("Error al paginar:", error);
            if (contenedor)
                contenedor.innerHTML = '<p class="text-red-500">Error al cargar.</p>';
        }
    });
}
window.cargarDatos = cargarDatos;
window.cargarActividad = cargarActividad;
//# sourceMappingURL=cargarActividad.js.map