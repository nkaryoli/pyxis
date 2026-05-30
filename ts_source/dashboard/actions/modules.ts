import type { DashboardContext } from "../types.js";
import { actualizarModulo, crearModulo, eliminarModulo } from "../api.js";

// Modal de edición/creación de módulos
const modal = document.getElementById("modal-modulo") as HTMLDialogElement;
const form = document.getElementById("form-modulo") as HTMLFormElement;
const mTxtTitulo = document.getElementById("modal-modulo-titulo")!;
const mInputCodigo = document.getElementById("modal-modulo-codigo") as HTMLInputElement;
const mInputNombre = document.getElementById("modal-modulo-nombre") as HTMLInputElement;
const mInputCursoAnio = document.getElementById("modal-modulo-curso-anio") as HTMLSelectElement;
const mInputCursoCarrera = document.getElementById("modal-modulo-curso-carrera") as HTMLSelectElement;
const mInputMode = document.getElementById("modal-modulo-mode") as HTMLInputElement;
const btnCancelar = document.getElementById("btn-cancelar-modulo");

// Modal de visualización de alumnos por módulo
const modalAlumnos = document.getElementById("modal-alumnos-modulo") as HTMLDialogElement;
const mTxtAlumnosTitulo = document.getElementById("modal-alumnos-modulo-titulo")!;
const mContainerAlumnosLista = document.getElementById("modal-alumnos-lista")!;
const btnCerrarAlumnos = document.getElementById("btn-cerrar-alumnos-modal");

btnCancelar?.addEventListener("click", () => modal.close());
btnCerrarAlumnos?.addEventListener("click", () => modalAlumnos.close());

form?.addEventListener("submit", (e) => {
	e.preventDefault();

	const codigo = mInputCodigo.value.trim();
	const nombre = mInputNombre.value.trim();
	const curso = `${mInputCursoAnio.value} ${mInputCursoCarrera.value}`;
	const mode = mInputMode.value;

	if (!codigo || !nombre || !curso) return;

	if (mode === "edit") {
		void actualizarModulo(codigo, {
			nombre_asignatura: nombre,
			curso_modulo: curso,
			rol_usuario_activo: "ADMINISTRADOR",
		})
		.then(() => {
			modal.close();
			location.reload();
		})
		.catch((err: Error) => alert(`No se pudo editar el módulo: ${err.message}`));
	} else {
		void crearModulo({
			codigo_modulo: codigo,
			nombre_asignatura: nombre,
			curso_modulo: curso,
			rol_usuario_activo: "ADMINISTRADOR",
		})
		.then(() => {
			modal.close();
			location.reload();
		})
		.catch((err: Error) => alert(`No se pudo crear el módulo: ${err.message}`));
	}
});

export function handleModuleAction(
	button: HTMLButtonElement,
	context: DashboardContext,
): boolean {
	const action = button.dataset.action;

	if (action === "crear-modulo") {
		form.reset();
		mInputMode.value = "create";
		mInputCodigo.value = "";
		mInputCodigo.readOnly = false;
		mTxtTitulo.textContent = "Crear Nuevo Módulo";
		modal.showModal();
		return true;
	}

	if (action === "editar-modulo") {
		const codigo = button.dataset.codigo;
		if (!codigo) return true;

		form.reset();
		mInputMode.value = "edit";
		mInputCodigo.value = codigo;
		mInputCodigo.readOnly = true;
		mTxtTitulo.textContent = "Editar Módulo";

		const row = button.closest("tr");
		if (row) {
			const cells = row.querySelectorAll("td");
			if (cells.length >= 3) {
				mInputNombre.value = cells[1]!.textContent?.trim() || "";
				const cursoCell = cells[2]!.textContent?.trim() || "";
				const parts = cursoCell.split(/\s+/);
				mInputCursoAnio.value = parts[0] || "1º";
				mInputCursoCarrera.value = parts[1] || "DAW";
			}
		}

		modal.showModal();
		return true;
	}

	if (action === "ver-alumnos-modulo") {
		const codigo = button.dataset.codigo;
		const nombre = button.dataset.nombre || codigo;
		if (!codigo) return true;

		mTxtAlumnosTitulo.textContent = `Alumnos matriculados en ${nombre}`;
		mContainerAlumnosLista.innerHTML = '<p class="text-zinc-400 text-sm py-4 text-center">Cargando alumnos...</p>';
		modalAlumnos.showModal();

		fetch(`/api/modulos/${encodeURIComponent(codigo)}/alumnos`)
		.then((res) => {
			if (!res.ok) throw new Error("Error al cargar la lista de alumnos.");
			return res.json() as Promise<{ id_usuario: number; username: string; email: string }[]>;
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
		.catch((err: Error) => {
			console.error(err);
			mContainerAlumnosLista.innerHTML = `<p class="text-red-400 text-sm py-4 text-center">No se pudo cargar la lista: ${err.message}</p>`;
		});

		return true;
	}

	if (action === "eliminar-modulo") {
		const codigo = button.dataset.codigo;
		if (!codigo || !confirm(`¿Eliminar el módulo ${codigo}?`)) return true;

		void eliminarModulo(codigo, context.userRole)
		.then(() => location.reload())
		.catch((err: Error) => alert(`No se pudo eliminar el módulo: ${err.message}`));
		return true;
	}

	return false;
}
