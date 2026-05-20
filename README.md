# Pyxis 

Bienvenido al repositorio de **Pyxis**, una plataforma de colaboración para estudiantes donde resolver dudas organizadas por módulos educativos. Este proyecto se desarrolla bajo la metodología ABP para el curso 2025-2026.

---

## Stack Tecnológico
* **Backend:** Flask (Python) con SQLAlchemy (ORM) y PyMySQL.
* **Frontend:** HTML5, Tailwind CSS y TypeScript (compilado a JS).
* **Base de Datos:** MySQL.

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

5. **Instalar las dependencias de Node:**
   ```bash
   pnpm install

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

Para trabajar de forma fluida en el proyecto, debes abrir 3 terminales distintas en la raíz del proyecto y ejecutar un comando en cada una. Esto mantendrá el servidor levantado y compilará de forma automática cualquier cambio que hagas en el frontend:

- **Terminal 1:** Servidor Flask (Asegúrate de tener el entorno virtual activado aquí antes de lanzar el comando)
   ```bash
   flask --app "src:create_app" run --debug

- **Terminal 2:** Compilación interactiva de TypeScript
   ```bash
   npm run ts:watch
   
- **Terminal 3:** Compilación interactiva de Tailwind CSS
   ```bash
   npm run tailwind:watch

## 👨‍💼 Autores

- **Karyoli Nieves:** [@nkaryoli](https://github.com/nkaryoli)
- **Marina Benach** [@BMarina4](https://github.com/nkaryoli](https://github.com/BMarina4))
- **Victor Alcrudo** [@Krudoner](https://github.com/nkaryoli](https://github.com/Krudoner))
- **Josep Fontanet** [@Nrk-92](https://github.com/nkaryoli](https://github.com/Nrk-92))