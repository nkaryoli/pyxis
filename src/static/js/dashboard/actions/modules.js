import { actualizarModulo, crearModulo, eliminarModulo } from "../api.js";
import { mostrarConfirmacion } from "../confirm.js";
import { guardarToastPendiente } from "../toast.js";
// Modal de edición/creación de módulos
const modal = document.getElementById("modal-modulo");
const form = document.getElementById("form-modulo");
const mTxtTitulo = document.getElementById("modal-modulo-titulo");
const mInputCodigo = document.getElementById("modal-modulo-codigo");
const mInputNombre = document.getElementById("modal-modulo-nombre");
const mInputCursoAnio = document.getElementById("modal-modulo-curso-anio");
const mInputCursoCarrera = document.getElementById("modal-modulo-curso-carrera");
const mInputMode = document.getElementById("modal-modulo-mode");
const btnCancelar = document.getElementById("btn-cancelar-modulo");
const btnCancelarTop = document.getElementById("btn-cancelar-modulo-top");
// Elementos del selector custom de Año
const btnCustomCursoAnio = document.getElementById("btn-custom-curso-anio");
const customCursoAnioValue = document.getElementById("custom-curso-anio-value");
const customCursoAnioOptions = document.getElementById("custom-curso-anio-options");
// Elementos del selector custom de Carrera
const btnCustomCursoCarrera = document.getElementById("btn-custom-curso-carrera");
const customCursoCarreraValue = document.getElementById("custom-curso-carrera-value");
const customCursoCarreraOptions = document.getElementById("custom-curso-carrera-options");
function updateCustomCursoAnio(val) {
    if (!mInputCursoAnio)
        return;
    mInputCursoAnio.value = val;
    if (customCursoAnioValue)
        customCursoAnioValue.textContent = val;
}
function updateCustomCursoCarrera(val) {
    if (!mInputCursoCarrera)
        return;
    mInputCursoCarrera.value = val;
    if (customCursoCarreraValue)
        customCursoCarreraValue.textContent = val;
}
// Modal de visualización de alumnos por módulo
const modalAlumnos = document.getElementById("modal-alumnos-modulo");
const mTxtAlumnosTitulo = document.getElementById("modal-alumnos-modulo-titulo");
const mContainerAlumnosLista = document.getElementById("modal-alumnos-lista");
const btnCerrarAlumnos = document.getElementById("btn-cerrar-alumnos-modal");
const btnCerrarAlumnosTop = document.getElementById("btn-cerrar-alumnos-modal-top");
btnCancelar === null || btnCancelar === void 0 ? void 0 : btnCancelar.addEventListener("click", () => modal.close());
btnCancelarTop === null || btnCancelarTop === void 0 ? void 0 : btnCancelarTop.addEventListener("click", () => modal.close());
btnCerrarAlumnos === null || btnCerrarAlumnos === void 0 ? void 0 : btnCerrarAlumnos.addEventListener("click", () => modalAlumnos.close());
btnCerrarAlumnosTop === null || btnCerrarAlumnosTop === void 0 ? void 0 : btnCerrarAlumnosTop.addEventListener("click", () => modalAlumnos.close());
btnCustomCursoAnio === null || btnCustomCursoAnio === void 0 ? void 0 : btnCustomCursoAnio.addEventListener("click", (e) => {
    e.stopPropagation();
    customCursoAnioOptions === null || customCursoAnioOptions === void 0 ? void 0 : customCursoAnioOptions.classList.toggle("hidden");
});
customCursoAnioOptions === null || customCursoAnioOptions === void 0 ? void 0 : customCursoAnioOptions.addEventListener("click", (e) => {
    const target = e.target;
    const option = target.closest(".curso-anio-option");
    if (option) {
        const val = option.dataset.val || "1º";
        updateCustomCursoAnio(val);
        customCursoAnioOptions.classList.add("hidden");
    }
});
btnCustomCursoCarrera === null || btnCustomCursoCarrera === void 0 ? void 0 : btnCustomCursoCarrera.addEventListener("click", (e) => {
    e.stopPropagation();
    customCursoCarreraOptions === null || customCursoCarreraOptions === void 0 ? void 0 : customCursoCarreraOptions.classList.toggle("hidden");
});
customCursoCarreraOptions === null || customCursoCarreraOptions === void 0 ? void 0 : customCursoCarreraOptions.addEventListener("click", (e) => {
    const target = e.target;
    const option = target.closest(".curso-carrera-option");
    if (option) {
        const val = option.dataset.val || "DAW";
        updateCustomCursoCarrera(val);
        customCursoCarreraOptions.classList.add("hidden");
    }
});
document.addEventListener("click", (e) => {
    const target = e.target;
    if (customCursoAnioOptions && !customCursoAnioOptions.classList.contains("hidden") && !(btnCustomCursoAnio === null || btnCustomCursoAnio === void 0 ? void 0 : btnCustomCursoAnio.contains(target))) {
        customCursoAnioOptions.classList.add("hidden");
    }
    if (customCursoCarreraOptions && !customCursoCarreraOptions.classList.contains("hidden") && !(btnCustomCursoCarrera === null || btnCustomCursoCarrera === void 0 ? void 0 : btnCustomCursoCarrera.contains(target))) {
        customCursoCarreraOptions.classList.add("hidden");
    }
});
form === null || form === void 0 ? void 0 : form.addEventListener("submit", (e) => {
    e.preventDefault();
    const codigo = mInputCodigo.value.trim();
    const nombre = mInputNombre.value.trim();
    const curso = `${mInputCursoAnio.value} ${mInputCursoCarrera.value}`;
    const mode = mInputMode.value;
    if (!codigo || !nombre || !curso)
        return;
    if (mode === "edit") {
        void actualizarModulo(codigo, {
            nombre_asignatura: nombre,
            curso_modulo: curso,
            rol_usuario_activo: "ADMINISTRADOR",
        })
            .then(() => {
            modal.close();
            guardarToastPendiente("Asignatura actualizada con éxito", "success");
            location.reload();
        })
            .catch((err) => guardarToastPendiente(`No se pudo editar el módulo: ${err.message}`, "error"));
    }
    else {
        void crearModulo({
            codigo_modulo: codigo,
            nombre_asignatura: nombre,
            curso_modulo: curso,
            rol_usuario_activo: "ADMINISTRADOR",
        })
            .then(() => {
            modal.close();
            guardarToastPendiente("Asignatura creada con éxito", "success");
            location.reload();
        })
            .catch((err) => guardarToastPendiente(`No se pudo crear el módulo: ${err.message}`, "error"));
    }
});
export function handleModuleAction(button, context) {
    var _a, _b;
    const action = button.dataset.action;
    if (action === "crear-modulo") {
        form.reset();
        mInputMode.value = "create";
        mInputCodigo.value = "";
        mInputCodigo.readOnly = false;
        updateCustomCursoAnio("1º");
        updateCustomCursoCarrera("DAW");
        mTxtTitulo.textContent = "Crear Nuevo Módulo";
        modal.showModal();
        return true;
    }
    if (action === "editar-modulo") {
        const codigo = button.dataset.codigo;
        if (!codigo)
            return true;
        form.reset();
        mInputMode.value = "edit";
        mInputCodigo.value = codigo;
        mInputCodigo.readOnly = true;
        mTxtTitulo.textContent = "Editar Módulo";
        const row = button.closest("tr");
        if (row) {
            const cells = row.querySelectorAll("td");
            if (cells.length >= 3) {
                mInputNombre.value = ((_a = cells[1].textContent) === null || _a === void 0 ? void 0 : _a.trim()) || "";
                const cursoCell = ((_b = cells[2].textContent) === null || _b === void 0 ? void 0 : _b.trim()) || "";
                const parts = cursoCell.split(/\s+/);
                updateCustomCursoAnio(parts[0] || "1º");
                updateCustomCursoCarrera(parts[1] || "DAW");
            }
        }
        modal.showModal();
        return true;
    }
    if (action === "ver-alumnos-modulo") {
        const codigo = button.dataset.codigo;
        const nombre = button.dataset.nombre || codigo;
        if (!codigo)
            return true;
        mTxtAlumnosTitulo.textContent = `Alumnos matriculados en ${nombre}`;
        mContainerAlumnosLista.innerHTML = '<p class="text-zinc-400 text-sm py-4 text-center">Cargando alumnos...</p>';
        modalAlumnos.showModal();
        fetch(`/api/modulos/${encodeURIComponent(codigo)}/alumnos`)
            .then((res) => {
            if (!res.ok)
                throw new Error("Error al cargar la lista de alumnos.");
            return res.json();
        })
            .then((alumnos) => {
            mContainerAlumnosLista.innerHTML = "";
            if (alumnos.length === 0) {
                mContainerAlumnosLista.innerHTML = '<p class="text-zinc-500 text-sm py-4 text-center">No hay alumnos matriculados en este módulo.</p>';
                return;
            }
            alumnos.forEach((al) => {
                const item = document.createElement("div");
                item.className = "flex items-center justify-between p-3 rounded bg-white/5 border border-white/5 hover:border-cyan-500/20 transition";
                item.innerHTML = `
					<div>
						<span class="text-xs font-mono text-cyan-300 mr-2">ID ${al.id_usuario}</span>
						<span class="text-sm font-semibold text-white">${al.username}</span>
					</div>
					<div class="text-xs text-zinc-400 font-mono">${al.email}</div>
				`;
                mContainerAlumnosLista.appendChild(item);
            });
        })
            .catch((err) => {
            console.error(err);
            mContainerAlumnosLista.innerHTML = `<p class="text-red-400 text-sm py-4 text-center">No se pudo cargar la lista: ${err.message}</p>`;
            guardarToastPendiente(`No se pudo cargar la lista: ${err.message}`, "error");
        });
        return true;
    }
    if (action === "eliminar-modulo") {
        const codigo = button.dataset.codigo;
        if (!codigo)
            return true;
        mostrarConfirmacion("Eliminar Asignatura", "¿Estás seguro de que deseas eliminar permanentemente esta asignatura?", () => {
            void eliminarModulo(codigo, context.userRole)
                .then(() => {
                guardarToastPendiente("Asignatura eliminada con éxito", "success");
                location.reload();
            })
                .catch((err) => guardarToastPendiente(`No se pudo eliminar el módulo: ${err.message}`, "error"));
        });
        return true;
    }
    return false;
}
//# sourceMappingURL=modules.js.map