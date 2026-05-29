import type { DashboardContext } from "../types.js";
import { actualizarUsuario, crearUsuario, eliminarUsuario } from "../api.js";

const modal = document.getElementById('modal-usuario') as HTMLDialogElement;
const form = document.getElementById('form-usuario') as HTMLFormElement;

const mTxtTitulo = document.getElementById('modal-titulo')!;
const mInputId = document.getElementById('modal-user-id') as HTMLInputElement;
const mInputEmail = document.getElementById('modal-email') as HTMLInputElement;
const mInputPassword = document.getElementById('modal-password') as HTMLInputElement;
const mInputRol = document.getElementById('modal-rol') as HTMLSelectElement;
const btnCancelar = document.getElementById('btn-cancelar-modal');
const passWrapper = document.getElementById('modal-pass-wrapper');

btnCancelar?.addEventListener('click', () => modal.close());

form?.addEventListener('submit', (e) => {
    e.preventDefault();

    const id = mInputId.value;
    const email = mInputEmail.value.trim();
    const password = mInputPassword.value;
    const rolUsuario = mInputRol.value;

    if (!email || !rolUsuario) return;

    if (id) {
        const payload: Record<string, string> = {
            email_usuario: email,
            rol: rolUsuario
        };

        const root = document.querySelector<HTMLElement>("[data-dashboard-root]");
        const solicitanteId = root?.dataset.userId ?? "";

        void actualizarUsuario(id, payload, solicitanteId)
            .then(() => {
                modal.close();
                location.reload();
            })
            .catch((err: Error) => alert(`No se pudo editar el usuario: ${err.message}`));
    } else {

        if (!password) {
            mInputPassword.required = true;
            return;
        }

        void crearUsuario({ email_usuario: email, password_usuario: password, rol: rolUsuario })
            .then(() => {
                modal.close();
                location.reload();
            })
            .catch((err: Error) => alert(`No se pudo crear el usuario: ${err.message}`));
    }
});

export function handleUserAction(
	button: HTMLButtonElement,
	context: DashboardContext,
): boolean {
	const action = button.dataset.action;
	if (action === "crear-usuario") {
		form.reset();
        mInputId.value = "";
        
        passWrapper?.classList.remove("hidden");
        mInputPassword.required = true;

        mTxtTitulo.textContent = "Crear Nuevo Usuario";
        
        modal.showModal();
        return true;
	}

	if (action === "editar-usuario") {
		const id = button.dataset.id;
		if (!id) return true;

        fetch(`/api/usuarios/${encodeURIComponent(id)}`)
            .then((res) => {
                if (!res.ok) throw new Error("Error al obtener la información del usuario.");
                return res.json() as Promise<{ id_usuario: number; username: string; email: string; rol: string }>;
            })
            .then((user) => {
                form.reset();
                mInputId.value = id;
                mInputEmail.value = user.email;
                mInputRol.value = user.rol;
                
                passWrapper?.classList.add("hidden");
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
		if (!id || !confirm(`¿Eliminar el usuario ${id}?`)) return true;

		void eliminarUsuario(id)
		.then(() => location.reload())
		.catch(() => alert("No se pudo eliminar el usuario con la API actual."));
		return true;
	}

	return false;
}
