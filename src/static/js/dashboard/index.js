/**
 * Punto de entrada principal para la interactividad del Dashboard.
 * Inicializa tabs, acciones, paginación, notificaciones y comportamientos globales de modales.
 */
import { getDashboardContext } from "./context.js";
import { initDashboardActions } from "./actions/index.js";
import { initDashboardTabs } from "./tabs.js";
import { initClientPagination } from "./pagination.js";
import { chequearToastsPendientes } from "./toast.js";
const context = getDashboardContext();
if (context) {
    initDashboardTabs(context);
    initDashboardActions(context);
    initClientPagination("seccion-modulos", 7);
    initClientPagination("seccion-usuarios", 7);
    initClientPagination("seccion-posts", 7);
    chequearToastsPendientes();
    document.addEventListener("click", (e) => {
        const target = e.target;
        const openDetails = document.querySelectorAll("details[open]");
        openDetails.forEach((details) => {
            if (!details.contains(target)) {
                details.open = false;
            }
        });
    });
    const updateBodyScroll = () => {
        const hasOpenDialog = Array.from(document.querySelectorAll("dialog")).some((dialog) => dialog.open);
        if (hasOpenDialog) {
            document.body.classList.add("overflow-hidden");
        }
        else {
            document.body.classList.remove("overflow-hidden");
        }
    };
    const dialogObserver = new MutationObserver(() => {
        updateBodyScroll();
    });
    document.querySelectorAll("dialog").forEach((dialog) => {
        dialogObserver.observe(dialog, { attributes: true, attributeFilter: ["open"] });
        dialog.addEventListener("close", updateBodyScroll);
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