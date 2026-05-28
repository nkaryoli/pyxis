import { PostType } from "../types/perfil.interface";

const ITEMS_PER_PAGE = 5;

interface Respuesta {
    id_respuesta: number;
    contenido_respuesta: string;
    fecha_creacion_respuesta: string;
    id_usuario: number;
    id_post: number;
}

interface Modulo {
    codigo_modulo: string;
    nombre_asignatura: string;
}

interface Item {
    type: 'post' | 'respuesta';
    id: number;
    titulo?: string;
    contenido: string;
    fecha: string;
    modulo?: string;
    id_post?: number;
    autor?: string;
    respuestas_count?: number;
    id_usuario?: number;
    usuario_respondedor?: string;
}

let notificacionesLeidas: Set<number> = new Set();
let modulosMap: Map<string, string> = new Map();

async function cargarModulos() {
    try {
        const response = await fetch('/api/modulos');
        const modulos: Modulo[] = await response.json();
        modulos.forEach((m: Modulo) => {
            modulosMap.set(m.codigo_modulo, m.nombre_asignatura);
        });
    } catch (error) {
        console.error("Error al cargar módulos:", error);
    }
}

function getNombreModulo(codigo: string): string {
    return modulosMap.get(codigo) || codigo || 'General';
}

function formatearFecha(fecha: string): string {
    try {
        // Intenta parsear la fecha en diferentes formatos
        let date: Date;
        
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
    } catch (error) {
        return 'Fecha no disponible';
    }
}

// Ordena los items más recientes primero
function ordenarItems(items: Item[]): Item[] {
    return [...items].sort((a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime());
}

function renderizarItems(items: Item[], containerSelector: string) {
    const contenedor = document.getElementById(containerSelector);
    if (!contenedor) return;
    
    contenedor.innerHTML = '';
    
    if (items.length === 0) {
        contenedor.innerHTML = `
            <div class="text-center py-10 border border-dashed border-zinc-800 rounded-xl">
                <p class="text-zinc-500">Aún no hay elementos publicados.</p>
            </div>`;
        return;
    }
    
    // Iteramos directamente sobre todos los items sin slice
    items.forEach((item: Item) => {
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

function renderizarNotificaciones(items: Item[], containerSelector: string) {
    const contenedor = document.getElementById(containerSelector);
    if (!contenedor) return;
    contenedor.innerHTML = '';
    const notificacionesArray = items.filter(i => i.type === 'respuesta');
    
    if (notificacionesArray.length === 0) {
        contenedor.innerHTML = `<div class="text-center py-10 border border-dashed border-zinc-800 rounded-xl"><p class="text-zinc-500">No hay notificaciones.</p></div>`;
        return;
    }
    
    notificacionesArray.forEach((notif: Item) => {
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

    (window as any).removerNotificacion = function(id: number) {
        const element = document.querySelector(`[onclick*="removerNotificacion(${id})"]`)?.parentElement;
        element?.remove();
    };
}
export async function cargarActividad(idUsuario: number) {
    try {
        await cargarModulos();
        const [postsRes, respRes, userRes] = await Promise.all([
            fetch(`/api/usuarios/${idUsuario}/posts`).then(r => r.json()),
            fetch(`/api/usuarios/${idUsuario}/respuestas`).then(r => r.json()),
            fetch('/auth/me', { headers: { 'Accept': 'application/json' } }).then(r => r.json())
        ]);
        
        const postsItems: Item[] = postsRes.map((p: any) => {
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
            const r = await fetch(`/api/posts/${item.id}/respuestas`).then(res => res.json());
            item.respuestas_count = r.length;
        }

        const respuestasItems: Item[] = [];
        for (const r of respRes) {
            const post = await fetch(`/api/posts/${r.id_post}`).then(res => res.json());
            respuestasItems.push({
                type: 'respuesta', id: r.id_respuesta, titulo: post.titulo_post, contenido: r.contenido_respuesta,
                fecha: r.fecha_respuesta, id_post: r.id_post, autor: userRes.username, 
                modulo: post.codigo_modulo
            });
        }

        const notifs: Item[] = [];
        for (const post of postsRes) {
            const resps = await fetch(`/api/posts/${post.id_post}/respuestas`).then(r => r.json());
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

        

    } catch (e) {
        console.error(e);
        ['content-destacados', 'content-posts', 'content-respuestas'].forEach(s => {
            const c = document.getElementById(s);
            if (c) c.innerHTML = '<p class="text-red-500 text-center py-10">Error al cargar.</p>';
        });
    }
}

