# Pyxis 

Bienvenido al repositorio de **Pyxis**, una plataforma de colaboración para estudiantes donde resolver dudas organizadas por módulos educativos. Este proyecto se desarrolla bajo la metodología ABP para el curso 2025-2026.

---

## Stack Tecnológico
* **Backend:** Flask (Python) con SQLAlchemy (ORM) y PyMySQL.
* **Frontend:** HTML5, Tailwind CSS y TypeScript (compilado a JS).
* **Base de Datos:** MySQL.
* **Testing:** pytest (Unit Tests) y Cypress (E2E Tests).

---

## Estructura del Proyecto (Arquitectura por Capas)

El proyecto utiliza el patrón *Application Factory* (`create_app()`) y está dividido en capas con responsabilidades claras para facilitar el desarrollo en equipo:

* `app.py`: Punto de entrada de la aplicación.
* `modules/`: Controladores y rutas de Flask (Blueprints) organizados por características.
* `models/`: Definición de los modelos de datos de SQLAlchemy (entidades).
* `repositories/`: Capa de acceso a datos (consultas y persistencia).
* `services/`: Lógica de negocio del foro.
* `templates/`: Plantillas HTML (vistas). Heredan de `base.html`.
* `ts_source/`: Código fuente en TypeScript antes de ser compilado.
* `static/`: Archivos estáticos finales (CSS de Tailwind y JS compilado).
* `sql/`: Scripts de la base de datos (creación de tablas e inserciones).
* `tests/`: Tests unitarios e integración del backend (pytest).
* `cypress/`: Tests E2E del frontend (Cypress).

---

## Configuración Inicial (Instalación)

1. **Clonar el repositorio y entrar al directorio:**
   ```bash
   git clone https://github.com/nkaryoli/pyxis.git
   cd pyxis

2. **Crear el entorno virtual de Python:**
   ```bash
   python -m venv venv

3. **Activar el entorno virtual:**

- En windows (PowerShell):
   ```bash
   .\venv\Scripts\Activate.ps1

- En Linux/Mac (PowerShell):
   ```bash
   source venv/bin/activate

- En windows (Git Bash):
   ```bash
   source /venv/Scripts/Activate

4. **Instalar las dependencias de Python:**
   ```bash
   pip install -r requirements.txt

5. **Instalar las dependencias de Node.js:**
   ```bash
   npm install

6. **Configurar las variables de entorno:**
Crea un archivo .env en la raíz del proyecto basándote en los datos de tu base de datos local:
   ```bash
   SECRET_KEY=cambiar_esto_en_produccion
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=tu_contrasena_aqui
   MYSQL_DB=abpTest

---

## Ejecución del Proyecto (Desarrollo en local)

Para trabajar de forma fluida en el proyecto, puedes elegir entre dos opciones:

**Opción A (Recomendada - 2 terminales):**

- **Terminal 1:** Servidor Flask (Asegúrate de tener el entorno virtual activado aquí antes de lanzar el comando)
   ```bash
   flask --app "src:create_app" run --debug

- **Terminal 2:** Combinación de watchers (TypeScript + Tailwind en paralelo)
   ```bash
   npm run watch

**Opción B (3 terminales separadas):**

- **Terminal 1:** Servidor Flask (Asegúrate de tener el entorno virtual activado aquí antes de lanzar el comando)
   ```bash
   flask --app "src:create_app" run --debug

- **Terminal 2:** Compilación interactiva de TypeScript
   ```bash
   npm run ts:watch
   
- **Terminal 3:** Compilación interactiva de Tailwind CSS
   ```bash
   npm run tailwind:watch

---

## Testing

El proyecto incluye dos tipos de tests:

### Unit Tests (Backend - pytest)

Los unit tests se encuentran en `tests/unit/` y prueban la lógica de servicios sin tocar la base de datos.

**Ejecutar:**
```bash
npm run test:unit
# o directamente
pytest tests/unit -v --cov=src
```

**Con cobertura (para CI/entrega):**
```bash
pytest tests/unit -v --cov=src --cov-report=term-missing
```

### E2E Tests (Frontend - Cypress)

Los E2E tests se encuentran en `cypress/e2e/` y prueban el flujo real del usuario en el navegador.

**Prerequisitos:**
- Asegúrate de que Flask está corriendo (`flask --app "src:create_app" run --debug`).

**Ejecutar (Interfaz gráfica):**
```bash
npm run cypress:open
# Selecciona el navegador y el spec a ejecutar en la ventana de Cypress.
```

**Ejecutar (Headless - terminal):**
```bash
npm run cypress:run
# o ejecutar un spec concreto:
npx cypress run --spec "cypress/e2e/pruebas.cy.js"
```

**Escribir nuevos tests:**
- Crea archivos `.cy.js` en `cypress/e2e/`.
- Usa `cy.visit()` para navegar, `cy.get()` para selectores, `cy.click()` para acciones.
- Ejemplo:
```javascript
describe('Mi feature', () => {
  it('hace algo', () => {
    cy.visit('/ruta')
    cy.get('#selector').click()
    cy.get('#resultado').should('be.visible')
  })
})
```

---

## 👨‍💼 Autores

- **Karyoli Nieves:** [@nkaryoli](https://github.com/nkaryoli)
- **Marina Benach** [@BMarina4](https://github.com/nkaryoli](https://github.com/BMarina4))
- **Victor Alcrudo** [@Krudoner](https://github.com/nkaryoli](https://github.com/Krudoner))
- **Josep Fontanet** [@Nrk-92](https://github.com/nkaryoli](https://github.com/Nrk-92))