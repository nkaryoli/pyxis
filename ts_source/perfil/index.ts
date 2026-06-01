/**
 * Punto de entrada principal para el perfil del usuario.
 * Expone las funciones necesarias al objeto window para su uso en Jinja2.
 */
import { cargarActividad, cargarDatos } from "./cargarActividad.js";
import { subirFoto } from "./perfil_subir_foto.js"

declare global {
  function cargarActividad(idUsuario: number): Promise<void>;
  function cargarDatos(containerId: string, page: number, idUsuario: number): Promise<void>;
  function subirFoto(input: HTMLInputElement, idUsuario: string): Promise<void>;
}

(window as any).cargarActividad = cargarActividad;
(window as any).cargarDatos = cargarDatos;
(window as any).subirFoto = subirFoto;