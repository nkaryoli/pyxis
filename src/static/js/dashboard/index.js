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
    document.addEventListener("click", (e) => {
        const target = e.target;
        const openDetails = document.querySelectorAll("details[open]");
        openDetails.forEach((details) => {
            if (!details.contains(target)) {
                details.open = false;
            }
        });
    });
}
//# sourceMappingURL=index.js.map