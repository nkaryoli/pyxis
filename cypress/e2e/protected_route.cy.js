describe('Protección de Rutas y Redirección Inteligente', () => {
	beforeEach(() => {
		// Nos aseguramos de un tamaño de escritorio
		cy.viewport(1280, 800)
		// Nos aseguramos de estar deslogueados eliminando cookies
		cy.clearCookies()
	})

	it('Al intentar acceder a la creación de post directamente, redirige a login', () => {
		cy.visit('/post/crear', { failOnStatusCode: false })
		
		// Debe redirigir al login
		cy.url().should('include', '/auth/login')
	})

	it('Al hacer click en "Crear post" en el sidebar como invitado, redirige a login', () => {
		cy.visit('/')

		// El botón de crear post en el sidebar
		cy.contains('a', 'Crear post').click({ force: true })

		// Debe redirigir automáticamente al login (nuestro fix)
		cy.url().should('include', '/auth/login')
	})

	it('Al intentar ver un perfil de usuario sin estar logueado, redirige a login', () => {
		cy.visit('/perfil/1', { failOnStatusCode: false })

		// Debe redirigir automáticamente al login
		cy.url().should('include', '/auth/login')
	})

	it('Intento de forzar por URL el acceso al dashboard de administración desde sesión de Alumno', () => {
		// 1. Iniciar sesión como ALUMNO (potter@pixys.com / hp123)
		cy.visit('/auth/login')
		cy.get('input[name="email_usuario"]').type('potter@pixys.com')
		cy.get('input[name="password_usuario"]').type('hp123')
		cy.get('input[name="email_usuario"]').closest('form').submit()

		// 2. Intentar acceder al dashboard (que requiere PROFESOR/ADMINISTRADOR)
		cy.visit('/dashboard', { failOnStatusCode: false })

		// 3. Comprobar que recibe un error de acceso denegado (403)
		cy.contains('403').should('be.visible')
	})

	it('Intento de forzar por URL el acceso a un perfil ajeno desde sesión de Alumno', () => {
		// 1. Iniciar sesión como ALUMNO (potter@pixys.com, id_usuario = 1)
		cy.visit('/auth/login')
		cy.get('input[name="email_usuario"]').type('potter@pixys.com')
		cy.get('input[name="password_usuario"]').type('hp123')
		cy.get('input[name="email_usuario"]').closest('form').submit()

		// 2. Intentar acceder al perfil de otro usuario (id_usuario = 2)
		cy.visit('/perfil/2', { failOnStatusCode: false })

		// 3. Comprobar que el servidor restringe el acceso (403)
		cy.contains('403').should('be.visible')
	})
})
