describe('Módulo Pruebas - E2E', () => {
	it('Carga las pruebas desde la API y muestra la lista', () => {
		cy.visit('/pruebas')
		cy.get('#cargarPruebas').click()
		// Esperar a que la lista se rellene (AJAX)
		cy.get('#listaPruebas').find('p').should('have.length.greaterThan', 0)
	})
})
