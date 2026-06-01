export function getDashboardContext() {
    var _a, _b;
    const root = document.querySelector("[data-dashboard-root]");
    if (!root)
        return null;
    const userId = (_a = root.dataset.userId) !== null && _a !== void 0 ? _a : "";
    const userRole = ((_b = root.dataset.userRole) !== null && _b !== void 0 ? _b : "").toUpperCase();
    const tabs = Array.from(document.querySelectorAll(".dashboard-tab"));
    const panels = Array.from(document.querySelectorAll("[data-dashboard-panel]"));
    return {
        root,
        userId,
        userRole,
        tabs,
        panels,
    };
}
//# sourceMappingURL=context.js.map