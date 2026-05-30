export function initClientPagination(
	containerId: string,
	rowsPerPage: number = 5
): void {
	const container = document.getElementById(containerId);
	if (!container) return;

	const table = container.querySelector("table");
	if (!table) return;

	const tbody = table.querySelector("tbody");
	if (!tbody) return;

	// Obtenemos todas las filas excluyendo la fila de "No hay elementos para mostrar" y de no-coincidencias
	const rows = Array.from(tbody.querySelectorAll("tr")).filter(
		(row) => !row.querySelector("td[colspan]") && !row.classList.contains("no-matches-row")
	);

	// Encontrar elementos de filtro dentro del contenedor
	const filters = Array.from(container.querySelectorAll<HTMLSelectElement | HTMLInputElement>(".table-filter"));

	// Crear fila de "No se han encontrado resultados" dinámicamente si no existe
	let noMatchesRow = tbody.querySelector(".no-matches-row") as HTMLTableRowElement | null;
	if (!noMatchesRow && rows.length > 0) {
		const cols = table.querySelectorAll("th").length || 6;
		noMatchesRow = document.createElement("tr");
		noMatchesRow.className = "no-matches-row hidden";
		noMatchesRow.innerHTML = `<td class="py-8 text-zinc-500 text-center" colspan="${cols}">No se han encontrado resultados coincidentes.</td>`;
		tbody.appendChild(noMatchesRow);
	}

	const controls = container.querySelector(".pagination-controls") as HTMLElement;

	let currentPage = 1;
	let activeRows = rows;
	let totalPages = Math.ceil(activeRows.length / rowsPerPage);

	const updateDisplay = () => {
		// Aplicar todos los filtros activos
		activeRows = rows.filter((row) => {
			for (const filter of filters) {
				const val = filter.value.trim().toLowerCase();
				if (!val) continue;

				const filterField = filter.dataset.filterField;
				if (filterField) {
					const cell = row.querySelector(`[data-field="${filterField}"]`);
					const cellText = cell?.textContent?.trim().toLowerCase() || "";
					if (filter instanceof HTMLInputElement) {
						if (!cellText.includes(val)) return false;
					} else {
						if (cellText !== val) return false;
					}
				} else {
					const rowText = row.textContent?.toLowerCase() || "";
					if (!rowText.includes(val)) return false;
				}
			}
			return true;
		});

		totalPages = Math.ceil(activeRows.length / rowsPerPage);

		// Ocultar todas las filas base primero
		rows.forEach((row) => row.classList.add("hidden"));

		// Mostrar u ocultar la fila de "No se han encontrado resultados"
		if (activeRows.length === 0 && rows.length > 0) {
			noMatchesRow?.classList.remove("hidden");
			if (controls) {
				controls.classList.add("hidden");
				controls.classList.remove("flex");
			}
			return;
		} else {
			noMatchesRow?.classList.add("hidden");
		}

		// Mostrar/ocultar los controles de paginación según corresponda
		if (totalPages <= 1) {
			if (controls) {
				controls.classList.add("hidden");
				controls.classList.remove("flex");
			}
		} else {
			if (controls) {
				controls.classList.remove("hidden");
				controls.classList.add("flex");
			}
		}

		// Limitar la página actual dentro de los rangos válidos
		if (currentPage > totalPages) currentPage = totalPages;
		if (currentPage < 1) currentPage = 1;

		// Mostrar las filas correspondientes a la página actual
		const start = (currentPage - 1) * rowsPerPage;
		const end = currentPage * rowsPerPage;

		activeRows.forEach((row, index) => {
			if (index >= start && index < end) {
				row.classList.remove("hidden");
			}
		});

		// Actualizar textos e interactividad de los botones de control
		if (controls) {
			const txtCurrent = controls.querySelector(".current-page-txt");
			const txtTotal = controls.querySelector(".total-pages-txt");
			if (txtCurrent) txtCurrent.textContent = String(currentPage);
			if (txtTotal) txtTotal.textContent = String(totalPages || 1);

			const btnPrev = controls.querySelector(".btn-prev") as HTMLButtonElement;
			const btnNext = controls.querySelector(".btn-next") as HTMLButtonElement;
			if (btnPrev) btnPrev.disabled = currentPage === 1;
			if (btnNext) btnNext.disabled = currentPage === totalPages;
		}
	};

	// Registrar listeners de controles de paginación si existen
	if (controls) {
		const btnPrev = controls.querySelector(".btn-prev") as HTMLButtonElement;
		const btnNext = controls.querySelector(".btn-next") as HTMLButtonElement;

		btnPrev?.addEventListener("click", () => {
			if (currentPage > 1) {
				currentPage--;
				updateDisplay();
			}
		});

		btnNext?.addEventListener("click", () => {
			if (currentPage < totalPages) {
				currentPage++;
				updateDisplay();
			}
		});
	}

	// Registrar listeners de filtros reactivos
	filters.forEach((filter) => {
		filter.addEventListener("change", () => {
			currentPage = 1;
			updateDisplay();
		});
		filter.addEventListener("input", () => {
			currentPage = 1;
			updateDisplay();
		});
	});

	// Inicialización
	updateDisplay();
}
