import { actualizarUsuario, crearUsuario, eliminarUsuario } from "../api.js";
const modal = document.getElementById('modal-usuario');
const form = document.getElementById('form-usuario');
const mTxtTitulo = document.getElementById('modal-titulo');
const mInputId = document.getElementById('modal-user-id');
const mInputEmail = document.getElementById('modal-email');
const mInputPassword = document.getElementById('modal-password');
const mInputRol = document.getElementById('modal-rol');
const btnCancelar = document.getElementById('btn-cancelar-modal');
const passWrapper = document.getElementById('modal-pass-wrapper');
btnCancelar === null || btnCancelar === void 0 ? void 0 : btnCancelar.addEventListener('click', () => modal.close());
form === null || form === void 0 ? void 0 : form.addEventListener('submit', (e) => {
    var _a;
    e.preventDefault();
    const id = mInputId.value;
    const email = mInputEmail.value.trim();
    const password = mInputPassword.value;
    const rolUsuario = mInputRol.value;
    if (!email || !rolUsuario)
        return;
    if (id) {
        const payload = {
            email_usuario: email,
            rol: rolUsuario
        };
        const root = document.querySelector("[data-dashboard-root]");
        const solicitanteId = (_a = root === null || root === void 0 ? void 0 : root.dataset.userId) !== null && _a !== void 0 ? _a : "";
        void actualizarUsuario(id, payload, solicitanteId)
            .then(() => {
            modal.close();
            location.reload();
        })
            .catch((err) => alert(`No se pudo editar el usuario: ${err.message}`));
    }
    else {
        if (!password) {
            mInputPassword.required = true;
            return;
        }
        void crearUsuario({ email_usuario: email, password_usuario: password, rol: rolUsuario })
            .then(() => {
            modal.close();
            location.reload();
        })
            .catch((err) => alert(`No se pudo crear el usuario: ${err.message}`));
    }
});
export function handleUserAction(button, context) {
    const action = button.dataset.action;
    if (action === "crear-usuario") {
        form.reset();
        mInputId.value = "";
        passWrapper === null || passWrapper === void 0 ? void 0 : passWrapper.classList.remove("hidden");
        mInputPassword.required = true;
        mTxtTitulo.textContent = "Crear Nuevo Usuario";
        modal.showModal();
        return true;
    }
    if (action === "editar-usuario") {
        const id = button.dataset.id;
        if (!id)
            return true;
        fetch(`/api/usuarios/${encodeURIComponent(id)}`)
            .then((res) => {
            if (!res.ok)
                throw new Error("Error al obtener la información del usuario.");
            return res.json();
        })
            .then((user) => {
            form.reset();
            mInputId.value = id;
            mInputEmail.value = user.email;
            mInputRol.value = user.rol;
            passWrapper === null || passWrapper === void 0 ? void 0 : passWrapper.classList.add("hidden");
            mInputPassword.value = "";
            mInputPassword.required = false;
            mTxtTitulo.textContent = "Editar Usuario";
            modal.showModal();
        })
            .catch((err) => {
            console.error(err);
            alert("No se pudo cargar la información del usuario para editar.");
        });
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