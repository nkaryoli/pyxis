import { actualizarUsuario, crearUsuario, eliminarUsuario } from "../api.js";
// Modal y Formulario de Usuario (Edición/Creación de credenciales)
const modal = document.getElementById('modal-usuario');
const form = document.getElementById('form-usuario');
const mTxtTitulo = document.getElementById('modal-titulo');
const mInputId = document.getElementById('modal-user-id');
const mInputEmail = document.getElementById('modal-email');
const mInputPassword = document.getElementById('modal-password');
const mInputRol = document.getElementById('modal-rol');
const btnCancelar = document.getElementById('btn-cancelar-modal');
const passWrapper = document.getElementById('modal-pass-wrapper');
// Modal y Formulario de Matrículas (Exclusivo para alumnos)
const modalMatricula = document.getElementById('modal-matricula');
const formMatricula = document.getElementById('form-matricula');
const mTxtMatriculaTitulo = document.getElementById('modal-matricula-titulo');
const mInputMatriculaUserId = document.getElementById('modal-matricula-user-id');
const btnCancelarMatricula = document.getElementById('btn-cancelar-matricula');
btnCancelar === null || btnCancelar === void 0 ? void 0 : btnCancelar.addEventListener('click', () => modal.close());
btnCancelarMatricula === null || btnCancelarMatricula === void 0 ? void 0 : btnCancelarMatricula.addEventListener('click', () => modalMatricula.close());
// Submit del Formulario de Usuario (Solo gestiona credenciales)
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
        void crearUsuario({
            email_usuario: email,
            password_usuario: password,
            rol: rolUsuario
        })
            .then(() => {
            modal.close();
            location.reload();
        })
            .catch((err) => alert(`No se pudo crear el usuario: ${err.message}`));
    }
});
// Submit del Formulario de Matriculaciones (Exclusivo para alumnos)
formMatricula === null || formMatricula === void 0 ? void 0 : formMatricula.addEventListener('submit', (e) => {
    var _a;
    e.preventDefault();
    const id = mInputMatriculaUserId.value;
    const modulosSeleccionados = Array.from(formMatricula.querySelectorAll('input[name="modulos_matricula"]:checked')).map((cb) => cb.value);
    if (!id)
        return;
    const root = document.querySelector("[data-dashboard-root]");
    const solicitanteId = (_a = root === null || root === void 0 ? void 0 : root.dataset.userId) !== null && _a !== void 0 ? _a : "";
    void actualizarUsuario(id, { modulos: modulosSeleccionados }, solicitanteId)
        .then(() => {
        modalMatricula.close();
        location.reload();
    })
        .catch((err) => alert(`No se pudo guardar la matrícula: ${err.message}`));
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
    if (action === "matricular-usuario") {
        const id = button.dataset.id;
        if (!id)
            return true;
        fetch(`/api/usuarios/${encodeURIComponent(id)}`)
            .then((res) => {
            if (!res.ok)
                throw new Error("Error al obtener la información del estudiante.");
            return res.json();
        })
            .then((user) => {
            formMatricula.reset();
            mInputMatriculaUserId.value = id;
            const checkboxes = formMatricula.querySelectorAll('input[name="modulos_matricula"]');
            checkboxes.forEach((cb) => cb.checked = false);
            if (user.modulos && Array.isArray(user.modulos)) {
                user.modulos.forEach((codigo) => {
                    const cb = formMatricula.querySelector(`input[name="modulos_matricula"][value="${codigo}"]`);
                    if (cb)
                        cb.checked = true;
                });
            }
            mTxtMatriculaTitulo.textContent = `Matricular a ${user.username}`;
            modalMatricula.showModal();
        })
            .catch((err) => {
            console.error(err);
            alert("No se pudo cargar la información de matrícula del estudiante.");
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