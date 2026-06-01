describe('Flujo de Registro E2E', () => {
	const timestamp = Date.now()
	const uniqueUsername = `cyuser${timestamp}`
	const uniqueEmail = `cyuser${timestamp}@monlau.com`
	const password = 'Password123!'

	beforeEach(() => {
		// Asegurar tamaño de escritorio
		cy.viewport(1280, 800)
	})

	it('Debe registrar un nuevo usuario con éxito y redirigir al login', () => {
		cy.visit('/auth/register')

		cy.get('input[name="email_usuario"]').type(uniqueEmail)
		cy.get('input[name="password_usuario"]').type(password)
		cy.get('input[name="confirm_password_usuario"]').type(password)

		cy.get('input[name="email_usuario"]').closest('form').submit()

		cy.url().should('include', '/auth/login')
	})

	it('No debe permitir enviar el formulario de registro si hay campos vacíos', () => {
		cy.visit('/auth/register')

		// Intentamos enviar el formulario vacío sin rellenar campos
		cy.get('input[name="email_usuario"]').closest('form').submit()

		// Debería permanecer en la página de registro
		cy.url().should('include', '/auth/register')
	})
})
