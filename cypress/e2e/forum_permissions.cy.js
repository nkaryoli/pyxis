describe("Pruebas de Permisos del Foro y Matriculación E2E", () => {
	before(() => {
		// Limpiar las respuestas de prueba previas creadas por Harry Potter (ID 1)
		// Intentamos usar `cy.task` (más portátil) y si falla, revertimos a `cy.exec`.
		cy.task("clearTestResponses", { force: false }).then((res) => {
		if (res && res.allowed === false) {
			cy.log("Task not allowed, falling back to cy.exec:", res.message);
			cy.exec("venv/Scripts/python scripts/clear_test_responses.py", {
			env: {
				PYTHONIOENCODING: "utf-8",
				ALLOW_DB_CLEAN: "1",
				FLASK_ENV: "testing",
			},
			failOnNonZeroExit: false,
			});
		} else {
			if (res && res.stdout) cy.log("clearTestResponses stdout:", res.stdout);
			else cy.log("clearTestResponses completed", res);
		}
		});
	});

	beforeEach(() => {
		// Asegurar tamaño de escritorio para evitar colapsos de menús
		cy.viewport(1280, 800);
		// Asegurar limpieza de cookies
		cy.clearCookies();

		// Iniciar sesión como Harry Potter (potter@pixys.com)
		cy.visit("/auth/login");
		cy.get('input[name="email_usuario"]').type("potter@pixys.com");
		cy.get('input[name="password_usuario"]').type("hp123");
		cy.get('input[name="email_usuario"]').closest("form").submit();
		cy.getCookie("auth_token").should("exist");

		// Interceptar peticiones críticas para esperar y asegurar sincronización
		cy.intercept("POST", "**/post/crear").as("postCrear");
		cy.intercept("POST", "**/posts/*/publicar").as("crearRespuesta");
		cy.intercept("POST", "**/respuestas/*/editar").as("editarRespuesta");
		cy.intercept("POST", "**/respuestas/*/eliminar").as("eliminarRespuesta");
		cy.intercept("POST", "**/api/posts/*/respuestas").as("apiCrearRespuesta");
	});

	it("1. Debe permitir crear un post si está matriculado en ese módulo y no mostrar módulos no matriculados en el select", () => {
		cy.visit("/post/crear");

		// Verificar que los módulos en los que está matriculado existen en el select
		cy.get("#codigo_modulo").find('option[value="MOD-BBDD"]').should("exist");
		cy.get("#codigo_modulo").find('option[value="MOD-PROG"]').should("exist");

		// Verificar que el módulo no matriculado (MOD-ENT) NO está en el select (comprobación robusta)
		cy.get("#codigo_modulo")
		.find("option")
		.then(($opts) => {
			const values = [...$opts].map((o) => o.value);
			expect(values).to.not.include("MOD-ENT");
		});

		// Crear un post en un módulo matriculado (MOD-PROG)
		const timestamp = Date.now();
		const titulo = `Duda Cypress E2E - Prog ${timestamp}`;
		const contenido = `Esta es una duda automatizada creada mediante Cypress en el módulo MOD-PROG con marca de tiempo ${timestamp}.`;

		cy.get("#codigo_modulo").select("MOD-PROG");
		cy.get("#titulo_post").type(titulo);
		cy.get("#contenido_post").type(contenido);

		cy.get("#titulo_post").closest("form").submit();

		// Esperar la respuesta del backend y luego verificar UI
		cy.wait("@postCrear");
		cy.url().should("include", "/posts");
		cy.contains(titulo).should("be.visible");
	});

	it("2. Debe bloquear por completo la creación forzada de un post en un módulo no matriculado (MOD-ENT) a nivel de backend", () => {
		// Simular una petición POST maliciosa/forzada para evadir los límites del frontend
		cy.getCookie("auth_token").then((cookie) => {
		cy.request({
			method: "POST",
			url: "/post/crear",
			form: true,
			body: {
			codigo_modulo: "MOD-ENT",
			titulo_post: "Duda Hackeada E2E",
			contenido_post:
				"Intento malicioso de publicar en un módulo donde no estoy matriculado.",
			},
			headers: { Cookie: `auth_token=${cookie.value}` },
			failOnStatusCode: false,
		}).then((response) => {
			// El servidor debe responder con un error de permisos (403) y no crear el post
			expect(response.status).to.eq(403);
			expect(String(response.body)).to.include("Acceso denegado");
		});
		});
	});

	it("3. Debe permitir responder a un post de módulo matriculado y bloquear respuesta en módulo no matriculado", () => {
		const timestamp = Date.now();
		const miRespuesta = `Comentario de prueba matriculado - ${timestamp}`;

		// CASO A: Responder en módulo MATRICULADO (MOD-BBDD, e.g., Post ID 3 "Examen")
		cy.visit("/posts/3");

		// Rellenar formulario de respuesta
		cy.get("#contenido_respuesta").type(miRespuesta);
		cy.get("#contenido_respuesta").closest("form").submit();
		cy.wait("@crearRespuesta");

		// Verificar que se redirecciona con éxito, muestra la alerta flash y el comentario aparece
		cy.url().should("include", "/posts/3");
		cy.contains("Respuesta publicada con éxito.").should("be.visible");
		// Comprobar backend vía API que la respuesta fue creada
		cy.request("GET", "/api/posts/3/respuestas").then((resp) => {
		expect(resp.status).to.eq(200);
		const found = resp.body.some(
			(r) =>
			r.contenido_respuesta &&
			r.contenido_respuesta.includes("Comentario de prueba matriculado"),
		);
		expect(found).to.be.true;
		});
		cy.reload();
		cy.contains("Comentario de prueba matriculado", { timeout: 10000 }).should(
		"be.visible",
		);

		// CASO B: Intentar responder en módulo NO MATRICULADO (MOD-ENT, e.g., Post ID 8 "Duda con Git Merge")
		cy.visit("/posts/8");

		// Intentar forzar el envío del comentario
		const intruso = `Intento intruso - ${timestamp}`;
		cy.get("#contenido_respuesta").type(intruso);
		cy.get("#contenido_respuesta").closest("form").submit();
		cy.wait("@crearRespuesta");

		// Debe alertar en la pantalla que no estamos matriculados
		cy.url().should("include", "/posts/8");
		cy.contains(
		"No estás matriculado en el módulo de este post. Solo puedes responder en posts de módulos donde estés matriculado.",
		).should("be.visible");

		// Comprobar que no se renderizó la respuesta intrusa en la lista
		cy.contains(intruso).should("not.exist");
	});

	it("4. Debe permitir editar y eliminar (soft-delete) su propia respuesta", () => {
		const timestamp = Date.now();
		const miRespuesta = `Comentario editable propio - ${timestamp}`;
		const miRespuestaEditada = `Comentario propio ACTUALIZADO - ${timestamp}`;

		// Crear respuesta
		cy.visit("/posts/3");

		cy.get("#contenido_respuesta").type(miRespuesta);
		cy.get("#contenido_respuesta").closest("form").submit();

		cy.wait("@crearRespuesta");

		// Verificar que realmente se guardó en backend
		cy.request("GET", "/api/posts/3/respuestas").then((resp) => {
		expect(resp.status).to.eq(200);

		const respuesta = resp.body.find(
			(r) =>
			r.contenido_respuesta && r.contenido_respuesta.includes(miRespuesta),
		);

		expect(respuesta, "respuesta creada en BD").to.exist;
		});

		// Determine which page contains the created response (server paginates 10 per page)
		cy.request("GET", "/api/posts/3/respuestas").then((resp) => {
		expect(resp.status).to.eq(200);
		const idx = resp.body.findIndex(
			(r) =>
			r.contenido_respuesta && r.contenido_respuesta.includes(miRespuesta),
		);
		expect(idx).to.be.greaterThan(-1);
		const perPage = 10;
		const page = Math.floor(idx / perPage) + 1;

		// Visit the page where the response is rendered and assert visibility
		cy.visit(`/posts/3?page=${page}`);
		cy.contains("Comentario editable propio", { timeout: 10000 }).should(
			"be.visible",
		);
		});

		// Editar nuestra respuesta
		cy.contains("div.p-5", miRespuesta).within(() => {
		cy.contains("a", "Editar").click();
		});

		cy.contains("div.p-5", miRespuesta).within(() => {
		cy.get('textarea[name="contenido_respuesta"]')
			.clear()
			.type(miRespuestaEditada);

		cy.contains("button", "Guardar").click();
		});

		cy.wait("@editarRespuesta");

		// Verificar edición en backend
		cy.wait(300);
		cy.request("GET", "/api/posts/3/respuestas").then((resp) => {
		expect(resp.status).to.eq(200);
		const respuestaEditada = resp.body.find(
			(r) =>
			r.contenido_respuesta &&
			r.contenido_respuesta.includes(miRespuestaEditada),
		);
		expect(respuestaEditada, "respuesta editada").to.exist;
		});

		cy.reload();

		// Use stable substring after edit to avoid exact-timestamp mismatches
		cy.contains("Comentario propio ACTUALIZADO", { timeout: 10000 }).should(
		"be.visible",
		);

		// Buscar el ID real y calcular la página ANTES de eliminar
		cy.request("GET", "/api/posts/3/respuestas").then((resp) => {
		const respuesta = resp.body.find(
			(r) =>
			r.contenido_respuesta &&
			r.contenido_respuesta.includes(miRespuestaEditada),
		);
		expect(respuesta).to.exist;

		const idx = resp.body.findIndex(
			(r) => r.id_respuesta === respuesta.id_respuesta,
		);
		const perPage = 10;
		const page = Math.floor(idx / perPage) + 1;

		cy.getCookie("auth_token").then((cookie) => {
			cy.request({
			method: "POST",
			url: `/respuestas/${respuesta.id_respuesta}/eliminar`,
			headers: {
				Cookie: `auth_token=${cookie.value}`,
			},
			failOnStatusCode: false,
			}).then((deleteResp) => {
			expect([200, 302]).to.include(deleteResp.status);

			// Visit the page where the response was and assert it no longer appears (soft-delete)
			cy.visit(`/posts/3?page=${page}`);
			cy.contains(miRespuestaEditada).should("not.exist");
			});
		});
		});
	});

	it("5. No debe permitir editar ni eliminar respuestas de otros usuarios", () => {
		// Visitar el Post ID 1 que tiene la respuesta original de Hermione ("El Inner solo trae coincidencias...")
		cy.visit("/posts/1");

		// Comprobar que la respuesta de Hermione no ofrece botones de edición ni eliminación a Harry
		cy.contains("div.p-5", "El Inner solo trae coincidencias...").within(() => {
		cy.contains("a", "Editar").should("not.exist");
		cy.contains("button", "Eliminar").should("not.exist");
		});

		// Intentar forzar la eliminación de la respuesta de Hermione (ID 1) directamente mediante una petición POST
		cy.getCookie("auth_token").then((cookie) => {
		cy.request({
			method: "POST",
			url: "/respuestas/1/eliminar",
			headers: { Cookie: `auth_token=${cookie.value}` },
			failOnStatusCode: false,
		}).then((response) => {
			// Comprobamos que el comentario de Hermione en el Post ID 1 sigue activo e intacto
			cy.visit("/posts/1");
			cy.contains("div.p-5", "El Inner solo trae coincidencias...").within(
			() => {
				cy.contains("span", "Eliminada").should("not.exist");
			},
			);
		});
		});
	});
});
