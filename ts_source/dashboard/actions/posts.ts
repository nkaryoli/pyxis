import type { DashboardContext } from "../types.js";
import { actualizarPost, eliminarPost } from "../api.js";
import { mostrarConfirmacion } from "../confirm.js";

const modal = document.getElementById("modal-post") as HTMLDialogElement;
const form = document.getElementById("form-post") as HTMLFormElement;
const mInputId = document.getElementById("modal-post-id") as HTMLInputElement;
const mInputTitulo = document.getElementById("modal-post-titulo-input") as HTMLInputElement;
const mInputContenido = document.getElementById("modal-post-contenido-input") as HTMLTextAreaElement;
const btnCancelar = document.getElementById("btn-cancelar-post");
const btnCancelarTop = document.getElementById("btn-cancelar-post-top");

btnCancelar?.addEventListener("click", () => modal.close());
btnCancelarTop?.addEventListener("click", () => modal.close());

form?.addEventListener("submit", (e) => {
	e.preventDefault();

	const id = mInputId.value;
	const titulo = mInputTitulo.value.trim();
	const contenido = mInputContenido.value.trim();

	if (!id || !titulo || !contenido) return;

	const root = document.querySelector<HTMLElement>("[data-dashboard-root]");
	const userId = root?.dataset.userId ?? "";
	const userRole = root?.dataset.userRole ?? "";

	void actualizarPost(id, { titulo_post: titulo, contenido_post: contenido }, userId, userRole)
	.then(() => {
		modal.close();
		location.reload();
	})
	.catch((err: Error) => alert(`No se pudo editar el post: ${err.message}`));
});

export function handlePostAction(
	button: HTMLButtonElement,
	context: DashboardContext,
): boolean {
	const action = button.dataset.action;

	if (action === "ver-post") {
		const id = button.dataset.id;
		if (!id) return true;
		window.location.href = `/posts/${encodeURIComponent(id)}`;
		return true;
	}

	if (action === "editar-post") {
		const id = button.dataset.id;
		if (!id) return true;

		form.reset();
		mInputId.value = id;

		fetch(`/api/posts/${encodeURIComponent(id)}`)
		.then((res) => {
			if (!res.ok) throw new Error("Error al obtener la información del post.");
			return res.json() as Promise<{ titulo_post: string; contenido_post: string }>;
		})
		.then((post) => {
			mInputTitulo.value = post.titulo_post;
			mInputContenido.value = post.contenido_post;
			modal.showModal();
		})
		.catch((err) => {
			console.error(err);
			alert("No se pudo cargar la información del post para editar.");
		});

		return true;
	}

	if (action === "eliminar-post") {
		const id = button.dataset.id;
		if (!id) return true;

		mostrarConfirmacion(
			"Eliminar Publicación",
			"¿Estás seguro de que deseas eliminar permanentemente esta publicación?",
			() => {
				void eliminarPost(id, context.userId, context.userRole)
					.then(() => location.reload())
					.catch((err: Error) => alert(`No se pudo eliminar el post: ${err.message}`));
			}
		);
		return true;
	}

	return false;
}
