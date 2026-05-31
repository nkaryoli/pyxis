let activeCallback: (() => void) | null = null;

/**
 * Muestra el modal de confirmación premium con un título y mensaje personalizados,
 * ejecutando el callback proporcionado únicamente si el usuario confirma la acción.
 */
export function mostrarConfirmacion(titulo: string, mensaje: string, callback: () => void): void {
	const modal = document.querySelector<HTMLDialogElement>("#modal-confirmacion");
	const txtTitulo = document.querySelector<HTMLHeadingElement>("#modal-confirmar-titulo");
	const txtMensaje = document.querySelector<HTMLParagraphElement>("#modal-confirmar-mensaje");
	const btnAceptar = document.querySelector<HTMLButtonElement>("#btn-confirmar-aceptar");
	const btnCancelar = document.querySelector<HTMLButtonElement>("#btn-confirmar-cancelar");
	const btnCancelarTop = document.querySelector<HTMLButtonElement>("#btn-confirmar-cancelar-top");

	if (!modal || !txtTitulo || !txtMensaje || !btnAceptar) return;

	txtTitulo.textContent = titulo;
	txtMensaje.textContent = mensaje;
	activeCallback = callback;

	// Función helper para cerrar de forma segura
	const cerrar = () => {
		modal.close();
	};

	// Asignamos la acción directa al hacer clic en Aceptar
	btnAceptar.onclick = () => {
		if (activeCallback) {
			activeCallback();
			activeCallback = null;
		}
		cerrar();
	};

	// Asignamos los cierres simples al Cancelar o pulsar la X
	if (btnCancelar) btnCancelar.onclick = cerrar;
	if (btnCancelarTop) btnCancelarTop.onclick = cerrar;

	modal.showModal();
}
