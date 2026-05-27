// ts_source/index.ts
import { cargarActividad } from "./cargarActividad.js";
import { subirFoto } from "./perfil_subir_foto.js";
// import { setupPostModalHandler } from "./cargarActividad.js";
// ... importa todas tus funciones

declare global {
  function cargarActividad(idUsuario: number): Promise<void>;
  function subirFoto(input: HTMLInputElement, idUsuario: string): Promise<void>;
  // ... declara todas las funciones
}

(window as any).cargarActividad = cargarActividad;
(window as any).subirFoto = subirFoto;
// Inicializar handler global de posts para mostrar modal (sin cambiar navegación backend)
// setupPostModalHandler();
// ... asigna todas 