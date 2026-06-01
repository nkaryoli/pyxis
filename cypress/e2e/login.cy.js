describe('Flujo de Login y Logout E2E', () => {
	beforeEach(() => {
		// Asegurar tamaño de escritorio
		cy.viewport(1280, 800)
		// Asegurar estar deslogueado
		cy.clearCookies()
	})

	it('Debe iniciar sesión correctamente con el usuario de pruebas ID 1 (potter@pixys.com)', () => {
		cy.visit('/auth/login')

		// Rellenar formulario de login
		cy.get('input[name="email_usuario"]').type('potter@pixys.com')
		cy.get('input[name="password_usuario"]').type('hp123')

		// Enviar login (usando el formulario específico del input para evitar conflictos de múltiples forms)
		cy.get('input[name="email_usuario"]').closest('form').submit()

		// Debería haberse creado la cookie de sesión
		cy.getCookie('auth_token').should('exist')
	})

	it('Debe mostrar un mensaje de error al introducir credenciales inválidas', () => {
		cy.visit('/auth/login')

		// Rellenar con credenciales incorrectas
		cy.get('input[name="email_usuario"]').type('potter@pixys.com')
		cy.get('input[name="password_usuario"]').type('WrongPassword123!')

		// Enviar login
		cy.get('input[name="email_usuario"]').closest('form').submit()

		// Debería permanecer en login, no tener la cookie de sesión y mostrar el error
		cy.url().should('include', '/auth/login')
		cy.getCookie('auth_token').should('not.exist')
		cy.contains('Credenciales inválidas').should('be.visible')
	})

	it('Debe cerrar sesión correctamente y eliminar la cookie de sesión', () => {
		// Loguearse
		cy.visit('/auth/login')
		cy.get('input[name="email_usuario"]').type('potter@pixys.com')
		cy.get('input[name="password_usuario"]').type('hp123')
		cy.get('input[name="email_usuario"]').closest('form').submit()

		cy.getCookie('auth_token').should('exist')

		// Hacer click en logout (usando el formulario específico de la navbar)
		cy.visit('/')
		cy.get('form[action*="/auth/logout"]').first().submit()

		// La cookie auth_token ya no debería existir
		cy.getCookie('auth_token').should('not.exist')
	})
})
