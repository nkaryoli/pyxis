from src.repositories.usuario_repository import UsuarioRepository
from src.services.post_service import PostService

class UsuarioService:
    """Servicio de lógica de negocio para la gestión de Usuarios."""

    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        """Busca un usuario y lanza error si no existe."""
        # Cambio: Validamos que id_usuario no sea None antes de ir al Repository
        if id_usuario is None:
            raise ValueError("ID de usuario no proporcionado.")
        usuario = UsuarioRepository.get_by_id(id_usuario)
        if not usuario:
            raise ValueError(f"El usuario con ID {id_usuario} no existe.")
        posts = PostService.ver_posts_por_usuario(id_usuario)
        if not posts:
            print("No se encontraron posts")
        print(posts)
        return usuario, posts

    @staticmethod
    def obtener_puntos_usuario(id_usuario):
        """Extrae específicamente los tokens del usuario."""
        usuario = UsuarioService.obtener_usuario_por_id(id_usuario)
        return usuario.tokens

    @staticmethod
    def actualizar_usuario(id_usuario_destino, datos, usuario_id_solicitante):
        """
        Lógica de permisos avanzada corregida para tipos de datos.
        """
        print('el id del solicitante es ', usuario_id_solicitante)
        print('el id del destino es ', id_usuario_destino)
        
        # 1. Validamos que el solicitante exista
        solicitante = UsuarioService.obtener_usuario_por_id(usuario_id_solicitante)
        destino = UsuarioService.obtener_usuario_por_id(id_usuario_destino)

        datos_filtrados = {}

        # 2. IMPORTANTE: Usamos int() para que la comparación sea real (12 == 12)
        if solicitante.rol == 'ALUMNO':
            if int(id_usuario_destino) != int(usuario_id_solicitante):
                raise ValueError("Un alumno no puede editar los datos de otros usuarios.")
            
            elif int(id_usuario_destino) == int(usuario_id_solicitante) and 'imagen_usuario' in datos:
                datos_filtrados['imagen_usuario'] = datos['imagen_usuario']
                print("Datos a actualizar:", datos_filtrados)

        elif solicitante.rol in ['PROFESOR', 'ADMINISTRADOR']:           
            campos_prohibidos = ['id_usuario', 'fecha_alta']
            datos_filtrados = {k: v for k, v in datos.items() if k not in campos_prohibidos}                
            
            nuevo_email = datos_filtrados.get('email_usuario')
            if nuevo_email and nuevo_email != destino.email_usuario:
                if UsuarioRepository.get_by_email(nuevo_email):
                    raise ValueError("El nuevo email ya está en uso por otro usuario.")            
        
        if not datos_filtrados:
            raise ValueError("No se han proporcionado datos válidos para actualizar.")
            
        # 3. Este es el paso final que guarda la URL en la DB
        return UsuarioRepository.update(id_usuario_destino, datos_filtrados)

    @staticmethod
    def eliminar_usuario(id_usuario, usuario_rol):
        """Lógica para eliminar un usuario."""               
        
        if usuario_rol != 'ADMINISTRADOR':
            raise ValueError("No se puede eliminar a un usuario si no eres administrador.")
            
        return UsuarioRepository.delete(id_usuario)