document.addEventListener('DOMContentLoaded', () => {
	const toggleBtn = document.getElementById('sidebar-toggle');
	const wrapper = document.getElementById('sidebar-wrapper');
	const backdrop = document.getElementById('sidebar-backdrop');
	const hamburgerIcon = document.getElementById('hamburger-icon');
	const closeIcon = document.getElementById('close-icon');

	if (toggleBtn && wrapper && backdrop && hamburgerIcon && closeIcon) {
		const isSidebarOpen = () => !wrapper.classList.contains('-translate-x-full');

		const openSidebar = () => {
			wrapper.classList.remove('-translate-x-full');
			wrapper.classList.add('translate-x-0');
			backdrop.classList.remove('hidden');
			document.body.classList.add('overflow-hidden');
			
			hamburgerIcon.classList.replace('block', 'hidden');
			closeIcon.classList.replace('hidden', 'block');
		};

		const closeSidebar = () => {
			wrapper.classList.remove('translate-x-0');
			wrapper.classList.add('-translate-x-full');
			backdrop.classList.add('hidden');
			document.body.classList.remove('overflow-hidden');
			
			hamburgerIcon.classList.replace('hidden', 'block');
			closeIcon.classList.replace('block', 'hidden');
		};

		toggleBtn.addEventListener('click', () => {
			if (isSidebarOpen()) {
				closeSidebar();
			} else {
				openSidebar();
			}
		});

		backdrop.addEventListener('click', closeSidebar);
	}
});
