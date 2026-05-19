document.addEventListener('DOMContentLoaded', () => {
    const boton = document.getElementById('cargarPruebas');
    const lista = document.getElementById('listaPruebas');

    if (!boton || !lista) return;

    boton.addEventListener('click', async () => {
        lista.innerHTML = '<p>Cargando...</p>';

        try {
            const respuesta = await fetch('/pruebas/api/pruebas');
            const pruebas = await respuesta.json();

            if (!Array.isArray(pruebas) || pruebas.length === 0) {
                lista.innerHTML = '<p>No hay pruebas disponibles.</p>';
                return;
            }

            lista.innerHTML = pruebas.map((prueba: any) => `
                <div class="bg-zinc-900 border border-zinc-700 rounded-lg p-4 text-white">
                    <h2 class="text-xl font-semibold">${prueba.titulo}</h2>
                    <p class="text-zinc-300 mt-2">${prueba.descripcion}</p>
                </div>
            `).join('');
        } catch (error) {
            console.error(error);
            lista.innerHTML = '<p>Error al cargar las pruebas.</p>';
        }
    });
});