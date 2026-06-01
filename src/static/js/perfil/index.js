/**
 * Punto de entrada principal para el perfil del usuario.
 * Expone las funciones necesarias al objeto window para su uso en Jinja2.
 */
import { cargarActividad, cargarDatos } from "./cargarActividad.js";
import { subirFoto } from "./perfil_subir_foto.js";
window.cargarActividad = cargarActividad;
window.cargarDatos = cargarDatos;
window.subirFoto = subirFoto;
//# sourceMappingURL=index.js.map