/**
 * Sube el archivo físico de la foto al servidor.
 * Versión final optimizada para Flask y Jinja2.
 */
export async function subirFoto(input: HTMLInputElement, usuarioId: number | string) {
    // 1. Verificamos que el input contenga un archivo
    if (!input.files || input.files.length === 0) return;
    const file = input.files[0];
    if (!file) return;

    // 2. Validación de tipo de archivo (Seguridad en cliente)
    const tiposPermitidos: string[] = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (tiposPermitidos.indexOf(file.type) === -1) {
        alert("Por favor, selecciona un archivo de imagen válido (JPG, PNG, WEBP).");
        return;
    }

    // 3. Validación de tamaño (Máximo 2MB)
    if (file.size > 2 * 1024 * 1024) {
        alert("La imagen es demasiado grande (máximo 2MB)");
        return;
    }

    // 4. Construcción del objeto FormData para envío de archivos binarios
    const formData = new FormData();
    formData.append('foto', file);

    try {
        // 5. Envío de la petición al endpoint de la API
        // IMPORTANTE: No definas 'Content-Type' manualmente; al pasar formData, 
        // el navegador establece automáticamente el boundary necesario.
        const response = await fetch(`/api/usuarios/${usuarioId}/foto`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-User-Id': usuarioId.toString() // Identificador necesario para el Service
            }
        });

        // 6. Procesamiento de la respuesta
        const data = await response.json();

        if (response.ok) {
            console.log("Éxito al subir:", data.url);
            // Forzamos la recarga de la página para que Jinja2 muestre la nueva ruta guardada en la DB
            window.location.reload(); 
        } else {
            // Manejo de errores controlados por el servidor
            alert(`Error: ${data.error || 'No se pudo subir la imagen'}`);
        }
    } catch (error) {
        // Manejo de errores de red o caídas del servidor
        console.error("Error de conexión:", error);
        alert("Error al conectar con el servidor. Verifica que Flask esté ejecutándose.");
    }
}

/** * NOTA DE INTEGRACIÓN:
 * Se ha omitido 'export { subirFoto }' para que la función sea accesible 
 * globalmente desde el atributo 'onchange' en tu archivo HTML/Jinja2.
 */