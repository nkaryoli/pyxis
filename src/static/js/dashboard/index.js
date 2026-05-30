import { getDashboardContext } from "./context.js";
import { initDashboardActions } from "./actions/index.js";
import { initDashboardTabs } from "./tabs.js";
import { initClientPagination } from "./pagination.js";
const context = getDashboardContext();
if (context) {
    initDashboardTabs(context);
    initDashboardActions(context);
    initClientPagination("seccion-modulos", 7);
    initClientPagination("seccion-usuarios", 7);
    initClientPagination("seccion-posts", 7);
    // Cierra los menús desplegables details abiertos al hacer clic fuera
    document.addEventListener("click", (e) => {
        const target = e.target;
        const openDetails = document.querySelectorAll("details[open]");
        openDetails.forEach((details) => {
            if (!details.contains(target)) {
                details.open = false;
            }
        });
    });
    // Gestiona el scroll del cuerpo de la página en función de los diálogos abiertos
    const updateBodyScroll = () => {
        const hasOpenDialog = Array.from(document.querySelectorAll("dialog")).some((dialog) => dialog.open);
        if (hasOpenDialog) {
            document.body.classList.add("overflow-hidden");
        }
        else {
            document.body.classList.remove("overflow-hidden");
        }
    };
    // Observa los cambios en el estado de apertura de los diálogos para bloquear/desbloquear el scroll
    const dialogObserver = new MutationObserver(() => {
        updateBodyScroll();
    });
    // Inicializa el cierre de diálogos al hacer clic fuera y el bloqueo de scroll
    document.querySelectorAll("dialog").forEach((dialog) => {
        dialogObserver.observe(dialog, { attributes: true, attributeFilter: ["open"] });
        // Escuchador nativo del evento de cierre para asegurar que el scroll se desbloquee
        dialog.addEventListener("close", updateBodyScroll);
        // Cierre al hacer clic fuera (solo clics en el backdrop translúcido)
        dialog.addEventListener("click", (event) => {
            if (event.target === dialog) {
                const rect = dialog.getBoundingClientRect();
                const isInDialog = (event.clientX >= rect.left &&
                    event.clientX <= rect.right &&
                    event.clientY >= rect.top &&
                    event.clientY <= rect.bottom);
                if (!isInDialog) {
                    dialog.close();
                }
            }
        });
    });
}
//# sourceMappingURL=index.js.map