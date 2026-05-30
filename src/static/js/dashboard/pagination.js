export function initClientPagination(containerId, rowsPerPage = 5) {
    const container = document.getElementById(containerId);
    if (!container)
        return;
    const table = container.querySelector("table");
    if (!table)
        return;
    const tbody = table.querySelector("tbody");
    if (!tbody)
        return;
    // Obtenemos todas las filas excluyendo la fila de "No hay elementos para mostrar"
    const rows = Array.from(tbody.querySelectorAll("tr")).filter((row) => !row.querySelector("td[colspan]"));
    const controls = container.querySelector(".pagination-controls");
    if (rows.length === 0) {
        if (controls) {
            controls.classList.add("hidden");
            controls.classList.remove("flex");
        }
        return;
    }
    const totalPages = Math.ceil(rows.length / rowsPerPage);
    if (totalPages <= 1) {
        if (controls) {
            controls.classList.add("hidden");
            controls.classList.remove("flex");
        }
        return;
    }
    else {
        if (controls) {
            controls.classList.remove("hidden");
            controls.classList.add("flex");
        }
    }
    let currentPage = 1;
    const btnPrev = controls.querySelector(".btn-prev");
    const btnNext = controls.querySelector(".btn-next");
    const txtCurrent = controls.querySelector(".current-page-txt");
    const txtTotal = controls.querySelector(".total-pages-txt");
    txtTotal.textContent = String(totalPages);
    const updateDisplay = () => {
        const start = (currentPage - 1) * rowsPerPage;
        const end = currentPage * rowsPerPage;
        rows.forEach((row, index) => {
            if (index >= start && index < end) {
                row.classList.remove("hidden");
            }
            else {
                row.classList.add("hidden");
            }
        });
        txtCurrent.textContent = String(currentPage);
        btnPrev.disabled = currentPage === 1;
        btnNext.disabled = currentPage === totalPages;
    };
    btnPrev.addEventListener("click", () => {
        if (currentPage > 1) {
            currentPage--;
            updateDisplay();
        }
    });
    btnNext.addEventListener("click", () => {
        if (currentPage < totalPages) {
            currentPage++;
            updateDisplay();
        }
    });
    // Inicialización
    updateDisplay();
}
//# sourceMappingURL=pagination.js.map