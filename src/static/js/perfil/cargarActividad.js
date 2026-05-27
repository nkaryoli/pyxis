var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
export function cargarActividad(idUsuario) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            // Cargar Posts
            const response = yield fetch(`/api/usuarios/${idUsuario}/posts`);
            const posts = yield response.json();
            const usuario_actual = yield fetch('/auth/me', {
                headers: {
                    'Accept': 'application/json'
                }
            });
            const usuario = yield usuario_actual.json();
            console.log(usuario);
            const contenedor = document.getElementById('content-posts');
            if (!contenedor)
                return;
            contenedor.innerHTML = '';
            if (posts.length > 0) {
                posts.forEach((post) => {
                    // Generamos el enlace usando la estructura que me diste de ejemplo
                    // Nota: Asegúrate de que '/posts/' sea la ruta correcta en tu backend
                    contenedor.innerHTML += `
                <a href="/posts/${post.id_post}" 
                   class="block mb-4 rounded-lg border border-zinc-800 bg-zinc-900/80 p-5 transition-all duration-300 hover:-translate-y-1 hover:border-cyan-500/50 group">
                    <div class="flex items-start justify-between gap-4">
                        <div>
                            <p class="text-xs uppercase tracking-[0.3em] text-cyan-400">
                                ${post.codigo_modulo || 'General'}
                            </p>
                            <h3 class="mt-2 text-lg font-semibold text-white group-hover:text-cyan-300">
                                ${post.titulo_post}
                            </h3>
                        </div>
                    </div>
                    <p class="mt-3 text-sm text-zinc-400 line-clamp-2">${post.contenido_post}</p>
                    <div class="mt-4 flex flex-wrap items-center gap-3 text-xs text-zinc-500">
                        <span>ID Post: ${post.id_post}</span>
                    </div>
                    <div class="mt-4 flex flex-wrap items-center gap-3 text-xs text-zinc-500">
                        <span>${usuario.username}</span>
                        <span>·</span>
                        <span>${post.fecha_creacion_post}</span>
                        <span>·</span>
                        <span> respuestas</span>
                    </div>
                </a>`;
                });
            }
            else {
                contenedor.innerHTML = `
                <div class="text-center py-10 border border-dashed border-zinc-800 rounded-xl">
                    <p class="text-zinc-500">Aún no hay posts publicados.</p>
                </div>`;
            }
        }
        catch (error) {
            console.error("Error al cargar la actividad:", error);
            const contenedor = document.getElementById('content-posts');
            if (contenedor) {
                contenedor.innerHTML =
                    '<p class="text-red-500 text-center py-10">Error al cargar los datos.</p>';
            }
        }
    });
}
//# sourceMappingURL=cargarActividad.js.map