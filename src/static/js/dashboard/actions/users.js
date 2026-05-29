import { actualizarUsuario, crearUsuario, eliminarUsuario } from "../api.js";
function promptValue(message, defaultValue = "") {
    const value = prompt(message, defaultValue);
    return value ? value.trim() : null;
}
export function handleUserAction(button, context) {
    const action = button.dataset.action;
    if (action === "crear-usuario") {
        const email = promptValue("Email del usuario");
        const password = promptValue("Contraseña temporal");
        const rolUsuario = promptValue("Rol (ALUMNO, PROFESOR, ADMINISTRADOR)", "ALUMNO");
        if (!email || !password || !rolUsuario)
            return true;
        void crearUsuario({ email_usuario: email, password_usuario: password, rol: rolUsuario })
            .then(() => location.reload())
            .catch(() => alert("No se pudo crear el usuario con la API actual."));
        return true;
    }
    if (action === "editar-usuario") {
        const id = button.dataset.id;
        if (!id)
            return true;
        const email = promptValue("Nuevo email (dejar vacío para mantener)");
        const username = promptValue("Nuevo username (dejar vacío para mantener)");
        const rolUsuario = promptValue("Nuevo rol (dejar vacío para mantener)");
        const payload = {};
        if (email)
            payload.email_usuario = email;
        if (username)
            payload.username = username;
        if (rolUsuario)
            payload.rol = rolUsuario;
        if (Object.keys(payload).length === 0)
            return true;
        void actualizarUsuario(id, payload, context.userId)
            .then(() => location.reload())
            .catch(() => alert("No se pudo editar el usuario con la API actual."));
        return true;
    }
    if (action === "eliminar-usuario") {
        const id = button.dataset.id;
        if (!id || !confirm(`¿Eliminar el usuario ${id}?`))
            return true;
        void eliminarUsuario(id)
            .then(() => location.reload())
            .catch(() => alert("No se pudo eliminar el usuario con la API actual."));
        return true;
    }
    return false;
}
//# sourceMappingURL=users.js.map