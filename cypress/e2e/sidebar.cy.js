describe('Sidebar Responsive y Drawer en Móvil E2E', () => {
	beforeEach(() => {
		cy.visit('/')
	})

	it('En pantallas de escritorio, el sidebar es visible y fijo', () => {
		cy.viewport(1280, 800)
		cy.get('#sidebar-wrapper').should('be.visible')
		cy.get('#sidebar-toggle').should('not.be.visible')
	})

	it('En pantallas móviles, el sidebar está colapsado e interactúa con el botón hamburguesa', () => {
		cy.viewport('iphone-x')
		cy.get('#sidebar-wrapper').should('not.be.visible')
		cy.get('#sidebar-toggle').should('be.visible').click()
		cy.get('#sidebar-wrapper').should('be.visible')
		cy.get('body').then(($body) => {
			if ($body.find('#sidebar-backdrop').length > 0) {
				cy.get('#sidebar-backdrop').click({ force: true })
				cy.get('#sidebar-wrapper').should('not.be.visible')
			}
		})
	})
})
