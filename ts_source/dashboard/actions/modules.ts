import type { DashboardContext } from "../types.js";
import { actualizarModulo, crearModulo, eliminarModulo } from "../api.js";

function promptValue(message: string): string | null {
	const value = prompt(message);
	return value ? value.trim() : null;
}

export function handleModuleAction(
	button: HTMLButtonElement,
	context: DashboardContext,
): boolean {
	const action = button.dataset.action;
	if (action === "crear-modulo") {
		const codigo = promptValue("Código del módulo");
		const nombre = promptValue("Nombre de la asignatura");
		const curso = promptValue("Curso del módulo");
		if (!codigo || !nombre || !curso) return true;

		void crearModulo({
			codigo_modulo: codigo,
			nombre_asignatura: nombre,
			curso_modulo: curso,
			rol_usuario_activo: "ADMINISTRADOR",
		})
		.then(() => location.reload())
		.catch(() => alert("No se pudo crear el módulo con la API actual."));
		return true;
	}

	if (action === "editar-modulo") {
		const codigo = button.dataset.codigo;
		const nombre = promptValue("Nuevo nombre de la asignatura");
		const curso = promptValue("Nuevo curso del módulo");
		if (!codigo || !nombre || !curso) return true;

		void actualizarModulo(codigo, { nombre_asignatura: nombre, curso_modulo: curso, rol_usuario_activo: "ADMINISTRADOR" })
		.then(() => location.reload())
		.catch(() => alert("No se pudo editar el módulo con la API actual."));
		return true;
	}

	if (action === "eliminar-modulo") {
		const codigo = button.dataset.codigo;
		if (!codigo || !confirm(`¿Eliminar el módulo ${codigo}?`)) return true;

		void eliminarModulo(codigo, context.userRole)
		.then(() => location.reload())
		.catch(() => alert("No se pudo eliminar el módulo con la API actual."));
		return true;
	}

	return false;
}
