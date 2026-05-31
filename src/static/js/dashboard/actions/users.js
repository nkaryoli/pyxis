import { actualizarUsuario, crearUsuario, eliminarUsuario } from "../api.js";
import { mostrarConfirmacion } from "../confirm.js";
import { guardarToastPendiente } from "../toast.js";
// Modal y Formulario de Usuario (Edición/Creación de credenciales)
const modal = document.getElementById('modal-usuario');
const form = document.getElementById('form-usuario');
const mTxtTitulo = document.getElementById('modal-titulo');
const mInputId = document.getElementById('modal-user-id');
const mInputEmail = document.getElementById('modal-email');
const mInputPassword = document.getElementById('modal-password');
const mInputRol = document.getElementById('modal-rol');
const btnCancelar = document.getElementById('btn-cancelar-modal');
const btnCancelarTop = document.getElementById('btn-cancelar-modal-top');
const passWrapper = document.getElementById('modal-pass-wrapper');
// Elementos del selector custom de rol
const btnCustomRol = document.getElementById('btn-custom-rol');
const customRolValue = document.getElementById('custom-rol-value');
const customRolOptions = document.getElementById('custom-rol-options');
function updateCustomRol(val) {
    if (!mInputRol)
        return;
    mInputRol.value = val;
    if (customRolValue) {
        const textMap = {
            'ALUMNO': 'Alumno',
            'PROFESOR': 'Profesor',
            'ADMINISTRADOR': 'Administrador'
        };
        customRolValue.textContent = textMap[val] || val;
    }
}
// Modal y Formulario de Matrículas (Exclusivo para alumnos)
const modalMatricula = document.getElementById('modal-matricula');
const formMatricula = document.getElementById('form-matricula');
const mTxtMatriculaTitulo = document.getElementById('modal-matricula-titulo');
const mInputMatriculaUserId = document.getElementById('modal-matricula-user-id');
const btnCancelarMatricula = document.getElementById('btn-cancelar-matricula');
const btnCancelarMatriculaTop = document.getElementById('btn-cancelar-matricula-top');
btnCancelar === null || btnCancelar === void 0 ? void 0 : btnCancelar.addEventListener('click', () => modal.close());
btnCancelarTop === null || btnCancelarTop === void 0 ? void 0 : btnCancelarTop.addEventListener('click', () => modal.close());
btnCancelarMatricula === null || btnCancelarMatricula === void 0 ? void 0 : btnCancelarMatricula.addEventListener('click', () => modalMatricula.close());
btnCancelarMatriculaTop === null || btnCancelarMatriculaTop === void 0 ? void 0 : btnCancelarMatriculaTop.addEventListener('click', () => modalMatricula.close());
btnCustomRol === null || btnCustomRol === void 0 ? void 0 : btnCustomRol.addEventListener('click', (e) => {
    e.stopPropagation();
    customRolOptions === null || customRolOptions === void 0 ? void 0 : customRolOptions.classList.toggle('hidden');
});
customRolOptions === null || customRolOptions === void 0 ? void 0 : customRolOptions.addEventListener('click', (e) => {
    const target = e.target;
    const option = target.closest('.rol-option');
    if (option) {
        const val = option.dataset.val || 'ALUMNO';
        updateCustomRol(val);
        customRolOptions.classList.add('hidden');
    }
});
document.addEventListener('click', (e) => {
    const target = e.target;
    if (customRolOptions && !customRolOptions.classList.contains('hidden') && !(btnCustomRol === null || btnCustomRol === void 0 ? void 0 : btnCustomRol.contains(target))) {
        customRolOptions.classList.add('hidden');
    }
});
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
            guardarToastPendiente("Usuario actualizado con éxito", "success");
            location.reload();
        })
            .catch((err) => guardarToastPendiente(`No se pudo editar el usuario: ${err.message}`, "error"));
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
            guardarToastPendiente("Usuario creado con éxito", "success");
            location.reload();
        })
            .catch((err) => guardarToastPendiente(`No se pudo crear el usuario: ${err.message}`, "error"));
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
        guardarToastPendiente("Matrículas actualizadas con éxito", "success");
        location.reload();
    })
        .catch((err) => guardarToastPendiente(`No se pudo guardar la matrícula: ${err.message}`, "error"));
});
export function handleUserAction(button, context) {
    var _a;
    const action = button.dataset.action;
    if (action === "crear-usuario") {
        form.reset();
        mInputId.value = "";
        updateCustomRol("ALUMNO");
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
            updateCustomRol(user.rol);
            passWrapper === null || passWrapper === void 0 ? void 0 : passWrapper.classList.add("hidden");
            mInputPassword.value = "";
            mInputPassword.required = false;
            mTxtTitulo.textContent = "Editar Usuario";
            modal.showModal();
        })
            .catch((err) => guardarToastPendiente(`No se pudo cargar la información del usuario para editar: ${err.message}`, "error"));
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
            .catch((err) => guardarToastPendiente(`No se pudo cargar la información de matrícula del estudiante: ${err.message}`, "error"));
        return true;
    }
    if (action === "eliminar-usuario") {
        const id = button.dataset.id;
        if (!id)
            return true;
        mostrarConfirmacion("Desactivar Usuario", "¿Estás seguro de que deseas desactivar este usuario?", () => {
            void eliminarUsuario(id)
                .then(() => {
                guardarToastPendiente("Usuario desactivado con éxito", "success");
                location.reload();
            })
                .catch(() => guardarToastPendiente("No se pudo desactivar el usuario.", "error"));
        });
        return true;
    }
    if (action === "restaurar-usuario") {
        const id = button.dataset.id;
        if (!id)
            return true;
        const root = document.querySelector("[data-dashboard-root]");
        const solicitanteId = (_a = root === null || root === void 0 ? void 0 : root.dataset.userId) !== null && _a !== void 0 ? _a : "";
        void actualizarUsuario(id, { is_active: true }, solicitanteId)
            .then(() => {
            guardarToastPendiente("Usuario activado con éxito", "success");
            location.reload();
        })
            .catch((err) => guardarToastPendiente(`No se pudo activar el usuario: ${err.message}`, "error"));
        return true;
    }
    return false;
}
//# sourceMappingURL=users.js.map