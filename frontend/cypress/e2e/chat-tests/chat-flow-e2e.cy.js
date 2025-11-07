describe("Flujo E2E del Chat SmartTalk", () => {

  beforeEach(() => {
    cy.visit("http://localhost:3000")
  })

  it("Validar la pantalla de inicio del chat", () => {
    cy.contains("Únete al Chat").should("be.visible")
    cy.get('input[placeholder*="nombre"]').should("be.visible")
    cy.contains("Entrar al Chat").should("be.visible")
    cy.screenshot("A1-pantalla-inicio")
  })

  it("Ingreso al chat con nombre 'John Cypress'", () => {
    cy.get('input[placeholder*="nombre"]').type("John Cypress")
    cy.contains("Entrar al Chat").click()
    cy.wait(2000)
    cy.screenshot("B1-chat-ingresado")
  })

  it("Escribir mensaje desde Cypress sin enviarlo", () => {
    cy.get('input[placeholder*="nombre"]').type("John Cypress")
    cy.contains("Entrar al Chat").click()
    cy.wait(2000)

    cy.contains("Chat Grupal").should("be.visible")

    cy.get('footer textarea, footer input, [placeholder*="Escribe"], [placeholder*="mensaje"]')
      .should("be.visible")
      .type("Mensaje escrito desde Cypress (sin enviar)")

    cy.screenshot("C1-mensaje-escrito")

    cy.wait(1000)
    cy.screenshot("C2-captura-final-sin-enviar")
  })

})
