// ts_source/index.ts
import { cargarActividad, cargarDatos } from "./cargarActividad.js";
import { subirFoto } from "./perfil_subir_foto.js"
// import { setupPostModalHandler } from "./cargarActividad.js";
// ... importa todas tus funciones

declare global {
  function cargarActividad(idUsuario: number): Promise<void>;
  function cargarDatos(containerId: string, page: number, idUsuario: number): Promise<void>; // Agrégala aquí
  function subirFoto(input: HTMLInputElement, idUsuario: string): Promise<void>;
}

(window as any).cargarActividad = cargarActividad;
(window as any).cargarDatos = cargarDatos;
(window as any).subirFoto = subirFoto;
// Inicializar handler global de posts para mostrar modal (sin cambiar navegación backend)
// setupPostModalHandler();
// ... asigna todas 