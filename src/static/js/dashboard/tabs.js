export function initDashboardTabs(context) {
    const { tabs, panels } = context;
    const activateTab = (targetId, updateHash = true) => {
        tabs.forEach((tab) => {
            const isActive = tab.dataset.tabTarget === targetId;
            tab.setAttribute("aria-selected", isActive ? "true" : "false");
            tab.classList.toggle("border-b-2", isActive);
            tab.classList.toggle("text-white", isActive);
            tab.classList.toggle("border-cyan-300", isActive);
            tab.classList.toggle("opacity-100", isActive);
            tab.classList.toggle("font-semibold", isActive);
        });
        panels.forEach((panel) => {
            panel.classList.toggle("hidden", panel.id !== targetId);
        });
        if (updateHash) {
            history.replaceState(null, "", `#${targetId}`);
        }
    };
    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            const targetId = tab.dataset.tabTarget;
            if (!targetId)
                return;
            activateTab(targetId);
        });
    });
    const hashInicial = window.location.hash.replace("#", "");
    const panelInicial = panels.some((panel) => panel.id === hashInicial) && hashInicial
        ? hashInicial
        : "seccion-modulos";
    activateTab(panelInicial, Boolean(window.location.hash));
}
//# sourceMappingURL=tabs.js.map