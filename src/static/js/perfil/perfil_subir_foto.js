var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
/**
 * Sube el archivo físico de la foto de perfil al servidor mediante FormData.
 *
 * @param input - Elemento HTML input tipo file.
 * @param usuarioId - Identificador del usuario.
 */
export function subirFoto(input, usuarioId) {
    return __awaiter(this, void 0, void 0, function* () {
        if (!input.files || input.files.length === 0)
            return;
        const file = input.files[0];
        if (!file)
            return;
        const tiposPermitidos = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
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
            const response = yield fetch(`/api/usuarios/${usuarioId}/foto`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-User-Id': usuarioId.toString()
                }
            });
            const data = yield response.json();
            if (response.ok) {
                console.log("Éxito al subir:", data.url);
                window.location.reload();
            }
            else {
                alert(`Error: ${data.error || 'No se pudo subir la imagen'}`);
            }
        }
        catch (error) {
            console.error("Error de conexión:", error);
            alert("Error al conectar con el servidor. Verifica que Flask esté ejecutándose.");
        }
    });
}
//# sourceMappingURL=perfil_subir_foto.js.map