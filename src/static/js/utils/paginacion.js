export function renderizarPaginador(containerId, currentPage, totalPages, idUsuario) {
    const contenedor = document.getElementById(containerId);
    if (!contenedor)
        return;
    let html = `<nav class="mt-4 flex gap-2">`;
    html += `<button ${currentPage <= 1 ? 'disabled' : ''} 
             onclick="cargarDatos('${containerId}', ${currentPage - 1}, ${idUsuario})"
             class="px-3 py-1 bg-gray-700 rounded disabled:opacity-50">Anterior</button>`;
    html += `<span class="px-3 py-1 text-cyan-400">Pág ${currentPage} de ${totalPages}</span>`;
    html += `<button ${currentPage >= totalPages ? 'disabled' : ''} 
             onclick="cargarDatos('${containerId}', ${currentPage + 1}, ${idUsuario})"
             class="px-3 py-1 bg-gray-700 rounded disabled:opacity-50">Siguiente</button>`;
    html += `</nav>`;
    contenedor.innerHTML += html;
}
//# sourceMappingURL=paginacion.js.map