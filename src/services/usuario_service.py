from src.repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    """Servicio de lógica de negocio para la gestión de Usuarios."""

    @staticmethod
    def obtener_usuario_por_id(id_usuario):
        """Busca un usuario y lanza error si no existe."""
        usuario = UsuarioRepository.get_by_id(id_usuario)
        if not usuario:
            raise ValueError(f"El usuario con ID {id_usuario} no existe.")
        return usuario

    @staticmethod
    def obtener_puntos_usuario(id_usuario):
        """Extrae específicamente los tokens del usuario."""
        usuario = UsuarioService.obtener_usuario_por_id(id_usuario)
        return usuario.tokens

    @staticmethod
    def crear_usuario(datos):
        """
        Crea un usuario con lógica profesional:
        - Autogenera username ignorando los 6 últimos caracteres antes de la @.
        - Valida dominios de Monlau.
        - Comprueba duplicados antes de insertar.
        """
        email = datos.get('email_usuario')
        password = datos.get('password_usuario')
        rol = datos.get('rol', 'ALUMNO')

        # 1. Validaciones básicas
        if not email or not password:
            raise ValueError("El email y la contraseña son obligatorios.")

        # 2. Validación de dominios oficiales
        dominios_validos = ['@monlau.com', '@campus.monlau.com', '@pixys.com']
        if not any(email.lower().endswith(domino) for domino in dominios_validos):
            raise ValueError("El email debe pertenecer a @monlau.com o @campus.monlau.com")

        # 3. Lógica de Username: victoralcaba@... -> victor
        parte_local = email.split('@')[0]
        # Si la parte local es muy corta (menor o igual a 6), no recortamos para no dejarlo vacío
        username_final = parte_local[:-6] if len(parte_local) > 6 else parte_local

        # 4. Comprobación profesional de duplicados
        # Verificar si el username ya existe
        # if UsuarioRepository.get_by_username(username_final):
        #     raise ValueError(f"El nombre de usuario '{username_final}' ya existe. Contacte con soporte.")
        
        # Verificar si el email ya existe
        if UsuarioRepository.get_by_email(email):
            raise ValueError("Este correo electrónico ya está registrado.")

        # 5. Guardado en Repositorio
        return UsuarioRepository.create(username_final, email, password, rol)

    @staticmethod
    def actualizar_usuario(id_usuario_destino, datos, usuario_id_solicitante):
        """
        Lógica de permisos avanzada:
        - ALUMNO: Solo propia foto.
        - PROFESOR/ADMIN: Todo sobre alumnos.
        """
        print('el id del solicitante es ', usuario_id_solicitante)
        print('el id del destino es ', id_usuario_destino)
        
        # id_solicitante = datos.get('id_solicitante') 
        solicitante = UsuarioService.obtener_usuario_por_id(usuario_id_solicitante)
        destino = UsuarioService.obtener_usuario_por_id(id_usuario_destino)

        datos_filtrados = {}

        if solicitante.rol == 'ALUMNO':
            if int(id_usuario_destino) != int(usuario_id_solicitante):
                raise ValueError("Un alumno no puede editar los datos de otros usuarios.")
            
            elif int(id_usuario_destino) == int(usuario_id_solicitante) and 'imagen_usuario' in datos:
                datos_filtrados['imagen_usuario'] = datos['imagen_usuario']
                print(datos_filtrados)
            # else:
            #     raise ValueError("Como alumno, solo puedes modificar tu foto de perfil.")

        elif solicitante.rol in ['PROFESOR', 'ADMINISTRADOR']:           

            # Solo prohibimos ID y Fecha. El email lo permitimos por si hubo error al teclear.
            campos_prohibidos = ['id_usuario', 'fecha_alta']
            datos_filtrados = {k: v for k, v in datos.items() if k not in campos_prohibidos}                
            nuevo_email = datos_filtrados.get('email_usuario')

            if nuevo_email and nuevo_email != destino.email_usuario:
                if UsuarioRepository.get_by_email(nuevo_email):
                    raise ValueError("El nuevo email ya está en uso por otro usuario.")            
        
            if not datos_filtrados:
                raise ValueError("No se han proporcionado datos válidos para actualizar.")
            
        return UsuarioRepository.update(id_usuario_destino, datos_filtrados)

    @staticmethod
    def eliminar_usuario(id_usuario, usuario_rol):
        """Lógica para eliminar un usuario."""               
        
        if usuario_rol != 'ADMINISTRADOR':

            raise ValueError("No se puede eliminar a un usuario si no eres administrador.")
            
        return UsuarioRepository.delete(id_usuario)
    
