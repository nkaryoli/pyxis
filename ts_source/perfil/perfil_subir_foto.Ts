/**
 * Sube el archivo físico de la foto de perfil al servidor mediante FormData.
 * 
 * @param input - Elemento HTML input tipo file.
 * @param usuarioId - Identificador del usuario.
 */
export async function subirFoto(input: HTMLInputElement, usuarioId: number | string) {
    if (!input.files || input.files.length === 0) return;
    const file = input.files[0];
    if (!file) return;

    const tiposPermitidos: string[] = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (tiposPermitidos.indexOf(file.type) === -1) {
        alert("Por favor, selecciona un archivo de imagen válido (JPG, PNG, WEBP).");
        return;
    }

    if (file.size > 2 * 1024 * 1024) {
        alert("La imagen es demasiado grande (máximo 2MB)");
        return;
    }

    const formData = new FormData();
    formData.append('foto', file);

    try {
        const response = await fetch(`/api/usuarios/${usuarioId}/foto`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-User-Id': usuarioId.toString()
            }
        });

        const data = await response.json();

        if (response.ok) {
            console.log("Éxito al subir:", data.url);
            window.location.reload(); 
        } else {
            alert(`Error: ${data.error || 'No se pudo subir la imagen'}`);
        }
    } catch (error) {
        console.error("Error de conexión:", error);
        alert("Error al conectar con el servidor. Verifica que Flask esté ejecutándose.");
    }
}