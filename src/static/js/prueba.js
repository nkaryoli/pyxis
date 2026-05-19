var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
document.addEventListener('DOMContentLoaded', () => {
    const boton = document.getElementById('cargarPruebas');
    const lista = document.getElementById('listaPruebas');
    if (!boton || !lista)
        return;
    boton.addEventListener('click', () => __awaiter(void 0, void 0, void 0, function* () {
        lista.innerHTML = '<p>Cargando...</p>';
        try {
            const respuesta = yield fetch('/pruebas/api/pruebas');
            const pruebas = yield respuesta.json();
            if (!Array.isArray(pruebas) || pruebas.length === 0) {
                lista.innerHTML = '<p>No hay pruebas disponibles.</p>';
                return;
            }
            lista.innerHTML = pruebas.map((prueba) => `
                <div class="bg-zinc-900 border border-zinc-700 rounded-lg p-4 text-white">
                    <h2 class="text-xl font-semibold">${prueba.titulo}</h2>
                    <p class="text-zinc-300 mt-2">${prueba.descripcion}</p>
                </div>
            `).join('');
        }
        catch (error) {
            console.error(error);
            lista.innerHTML = '<p>Error al cargar las pruebas.</p>';
        }
    }));
});
export {};
//# sourceMappingURL=prueba.js.map