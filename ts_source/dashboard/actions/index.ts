import type { DashboardContext } from "../types.js";
import { handleModuleAction } from "./modules.js";
import { handlePostAction } from "./posts.js";
import { handleUserAction } from "./users.js";

export function initDashboardActions(context: DashboardContext): void {
	document.addEventListener("click", (event) => {
		const target = event.target;
		if (!(target instanceof Element)) return;

		const button = target.closest<HTMLButtonElement>(".action-btn");
		if (!button) return;

		const handlers = [handleModuleAction, handlePostAction, handleUserAction];
		for (const handler of handlers) {
		if (handler(button, context)) return;
		}
	});
}
