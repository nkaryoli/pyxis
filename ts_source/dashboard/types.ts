export interface DashboardContext {
	root: HTMLElement;
	userId: string;
	userRole: string;
	tabs: HTMLButtonElement[];
	panels: HTMLElement[];
}

export type DashboardActionHandler = (
	button: HTMLButtonElement,
	context: DashboardContext,
) => boolean;
