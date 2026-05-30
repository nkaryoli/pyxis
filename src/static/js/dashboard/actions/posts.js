import { actualizarPost, eliminarPost } from "../api.js";
const modal = document.getElementById("modal-post");
const form = document.getElementById("form-post");
const mInputId = document.getElementById("modal-post-id");
const mInputTitulo = document.getElementById("modal-post-titulo-input");
const mInputContenido = document.getElementById("modal-post-contenido-input");
const btnCancelar = document.getElementById("btn-cancelar-post");
btnCancelar === null || btnCancelar === void 0 ? void 0 : btnCancelar.addEventListener("click", () => modal.close());
form === null || form === void 0 ? void 0 : form.addEventListener("submit", (e) => {
    var _a, _b;
    e.preventDefault();
    const id = mInputId.value;
    const titulo = mInputTitulo.value.trim();
    const contenido = mInputContenido.value.trim();
    if (!id || !titulo || !contenido)
        return;
    const root = document.querySelector("[data-dashboard-root]");
    const userId = (_a = root === null || root === void 0 ? void 0 : root.dataset.userId) !== null && _a !== void 0 ? _a : "";
    const userRole = (_b = root === null || root === void 0 ? void 0 : root.dataset.userRole) !== null && _b !== void 0 ? _b : "";
    void actualizarPost(id, { titulo_post: titulo, contenido_post: contenido }, userId, userRole)
        .then(() => {
        modal.close();
        location.reload();
    })
        .catch((err) => alert(`No se pudo editar el post: ${err.message}`));
});
export function handlePostAction(button, context) {
    const action = button.dataset.action;
    if (action === "ver-post") {
        const id = button.dataset.id;
        if (!id)
            return true;
        window.location.href = `/posts/${encodeURIComponent(id)}`;
        return true;
    }
    if (action === "editar-post") {
        const id = button.dataset.id;
        if (!id)
            return true;
        form.reset();
        mInputId.value = id;
        fetch(`/api/posts/${encodeURIComponent(id)}`)
            .then((res) => {
            if (!res.ok)
                throw new Error("Error al obtener la información del post.");
            return res.json();
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
        if (!id || !confirm(`¿Eliminar el post ${id}?`))
            return true;
        void eliminarPost(id, context.userId, context.userRole)
            .then(() => location.reload())
            .catch((err) => alert(`No se pudo eliminar el post: ${err.message}`));
        return true;
    }
    return false;
}
//# sourceMappingURL=posts.js.map