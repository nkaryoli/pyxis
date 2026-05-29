import { actualizarPost, eliminarPost } from "../api.js";
function promptValue(message) {
    const value = prompt(message);
    return value ? value.trim() : null;
}
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
        const titulo = promptValue("Nuevo título del post");
        const contenido = promptValue("Nuevo contenido del post");
        if (!titulo || !contenido)
            return true;
        void actualizarPost(id, { titulo_post: titulo, contenido_post: contenido }, context.userId, context.userRole)
            .then(() => location.reload())
            .catch(() => alert("No se pudo editar el post con la API actual."));
        return true;
    }
    if (action === "eliminar-post") {
        const id = button.dataset.id;
        if (!id || !confirm(`¿Eliminar el post ${id}?`))
            return true;
        void eliminarPost(id, context.userId, context.userRole)
            .then(() => location.reload())
            .catch(() => alert("No se pudo eliminar el post con la API actual."));
        return true;
    }
    return false;
}
//# sourceMappingURL=posts.js.map