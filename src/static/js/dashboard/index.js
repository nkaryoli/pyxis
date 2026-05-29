import { getDashboardContext } from "./context.js";
import { initDashboardActions } from "./actions/index.js";
import { initDashboardTabs } from "./tabs.js";
const context = getDashboardContext();
if (context) {
    initDashboardTabs(context);
    initDashboardActions(context);
}
//# sourceMappingURL=index.js.map