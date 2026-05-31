/**
 * Permite mostrar mensajes flotantes animados y soporta persistencia a través de recargas de página.
 */

export function mostrarToast(mensaje: string, tipo: 'success' | 'error' | 'warning' | 'info' = 'success'): void {
	// 1. Obtener o crear el contenedor global de toasts
	let container = document.getElementById("toast-container");
	if (!container) {
		container = document.createElement("div");
		container.id = "toast-container";
		container.className = "fixed bottom-5 right-5 z-[9999] flex flex-col gap-3 pointer-events-none max-w-sm w-full px-4 sm:px-0";
		document.body.appendChild(container);
	}

	// 2. Configurar clases estáticas literales de Tailwind para evitar fallos de compilación estática
	let borderClass = "border-cyan-500/20";
	let shadowClass = "shadow-cyan-500/15";
	let textClass = "text-cyan-400";
	let iconSvg = "";

	if (tipo === "success") {
		borderClass = "border-cyan-500/20";
		shadowClass = "shadow-cyan-500/5";
		textClass = "text-cyan-400";
		iconSvg = `<svg class="w-5 h-5 ${textClass}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
	} else if (tipo === "error") {
		borderClass = "border-red-500/20";
		shadowClass = "shadow-red-500/5";
		textClass = "text-red-400";
		iconSvg = `<svg class="w-5 h-5 ${textClass}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
	} else if (tipo === "warning") {
		borderClass = "border-amber-500/20";
		shadowClass = "shadow-amber-500/5";
		textClass = "text-amber-400";
		iconSvg = `<svg class="w-5 h-5 ${textClass}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>`;
	} else {
		borderClass = "border-blue-400/20";
		shadowClass = "shadow-blue-400/5";
		textClass = "text-blue-400";
		iconSvg = `<svg class="w-5 h-5 ${textClass}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
	}

	// 3. Crear el elemento toast
	const toast = document.createElement("div");
	toast.className = `flex flex-col overflow-hidden rounded-sm border bg-zinc-950/95 p-4 shadow-2xl transition-all duration-500 ease-out transform translate-y-8 opacity-0 pointer-events-auto cursor-pointer ${borderClass} ${shadowClass}`;
	
	// 4. Maquetación interna del Toast
	toast.innerHTML = `
		<div class="flex items-start gap-3">
			<div class="shrink-0">${iconSvg}</div>
			<div class="flex-1 text-sm font-medium text-zinc-200 pr-2 select-none">${mensaje}</div>
			<button type="button" class="text-zinc-500 hover:text-white transition-colors duration-150 text-base font-semibold leading-none select-none">
				×
			</button>
		</div>
	`;

	container.appendChild(toast);

	// 5. Controles de Cierre
	const btnCerrar = toast.querySelector("button");

	const cerrarToast = () => {
		toast.classList.remove("translate-y-0", "opacity-100");
		toast.classList.add("translate-y-8", "opacity-0");
		setTimeout(() => {
			toast.remove();
		}, 500);
	};

	if (btnCerrar) btnCerrar.onclick = (e) => {
		e.stopPropagation();
		cerrarToast();
	};
	toast.onclick = cerrarToast;

	// Forzar reflow para activar las transiciones CSS de entrada
	void toast.offsetWidth;

	// Mostrar con animación slide-up suave
	toast.classList.remove("translate-y-8", "opacity-0");
	toast.classList.add("translate-y-0", "opacity-100");

	// Auto-destrucción a los 3 segundos
	setTimeout(cerrarToast, 3000);
}

/**
 * Guarda temporalmente un toast en sessionStorage para ser ejecutado tras recargar la página.
 */
export function guardarToastPendiente(mensaje: string, tipo: 'success' | 'error' | 'warning' | 'info' = 'success'): void {
	sessionStorage.setItem("pending-toast", JSON.stringify({ mensaje, tipo }));
}

/**
 * Comprueba si existen notificaciones pendientes en sessionStorage y las renderiza al cargar.
 */
export function chequearToastsPendientes(): void {
	const pending = sessionStorage.getItem("pending-toast");
	if (pending) {
		try {
			const data = JSON.parse(pending) as { mensaje: string; tipo: 'success' | 'error' | 'warning' | 'info' };
			mostrarToast(data.mensaje, data.tipo);
		} catch (e) {
			console.error("Error al procesar la notificación pendiente:", e);
		}
		sessionStorage.removeItem("pending-toast");
	}
}
