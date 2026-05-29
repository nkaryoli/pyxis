import type { DashboardContext } from "./types.js";

export function getDashboardContext(): DashboardContext | null {
	const root = document.querySelector<HTMLElement>("[data-dashboard-root]");
	if (!root) return null;

	const userId = root.dataset.userId ?? "";
	const userRole = (root.dataset.userRole ?? "").toUpperCase();
	const tabs = Array.from(document.querySelectorAll<HTMLButtonElement>(".dashboard-tab"));
	const panels = Array.from(document.querySelectorAll<HTMLElement>("[data-dashboard-panel]"));

	return {
		root,
		userId,
		userRole,
		tabs,
		panels,
	};
}
