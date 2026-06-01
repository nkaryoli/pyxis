from src.repositories.modulo_repository import ModuloRepository

class ModuloService:
    """Servicio de lógica de negocio para la gestión de Módulos académicos."""

    @staticmethod
    def obtener_todos_los_modulos():
        """Obtiene todas las asignaturas de la base de datos."""
        from src.extensions import should_include_deleted
        return ModuloRepository.get_all(include_deleted=should_include_deleted())
    
    @staticmethod
    def obtener_modulo_por_codigo(codigo_modulo):
        """Busca una asignatura por su clave primaria string y valida su existencia."""
        if not codigo_modulo:
            raise ValueError("El código del módulo no puede estar vacío.")
        from src.extensions import should_include_deleted
        modulo = ModuloRepository.get_by_codigo(codigo_modulo.strip().upper(), include_deleted=should_include_deleted())
        if not modulo:
            raise ValueError(f"Módulo con código '{codigo_modulo}' no encontrado.")
        return modulo

    @staticmethod
    def obtener_modulo_por_nombre_modulo(nombre_modulo):
        """Busca una asignatura por su clave primaria string y valida su existencia."""
        if not nombre_modulo:
            raise ValueError("El nombre del módulo no puede estar vacío.")
        nombre_limpio = nombre_modulo.strip()
        from src.extensions import should_include_deleted
        modulo = ModuloRepository.get_by_name(nombre_limpio, include_deleted=should_include_deleted())
        if not modulo:
            raise ValueError(f"Módulo con nombre'{nombre_modulo}' no encontrado.")
        return modulo

    @staticmethod
    def obtener_posts_por_modulo(codigo_modulo):
        """Obtiene los posts asociados a un módulo."""
        from src.services.post_service import PostService
        return PostService.ver_posts_por_modulo(codigo_modulo)

    @staticmethod
    def obtener_detalle_modulo(nombre_modulo):
        """Devuelve el módulo resuelto y los posts preparados para la vista."""
        modulo = ModuloService.obtener_modulo_por_nombre_modulo(nombre_modulo)
        posts = ModuloService.obtener_posts_por_modulo(modulo.codigo_modulo)
        modulo.numero_posts = len(posts)
        return modulo, posts
    
    @staticmethod
    def crear_nuevo_modulo(codigo_modulo, nombre_asignatura, curso_modulo, rol_usuario):
        """
        Crea un nuevo módulo con validación de campos y rol.
        
        Args:
            codigo_modulo (str): Código del módulo.
            nombre_asignatura (str): Nombre del módulo.
            curso_modulo (str): Curso al que pertenece.
            rol_usuario (str): Rol del usuario que realiza la acción.
            
        Returns:
            Modulo: El objeto del módulo creado.
        """
        if rol_usuario not in ['PROFESOR', 'ADMINISTRADOR']:
            raise ValueError("Acceso denegado: Solo profesores y administradores pueden crear módulos.")
        
        if not codigo_modulo or not nombre_asignatura or not curso_modulo:
            raise ValueError("Todos los campos son obligatorios para crear un módulo.")
        
        codigo_limpio = codigo_modulo.strip().upper()
        nombre_limpio = nombre_asignatura.strip()
        curso_limpio = curso_modulo.strip()
        
        if len(codigo_limpio) < 3:
            raise ValueError("El código del módulo debe tener al menos 3 caracteres")
        if len(nombre_limpio) < 4:
            raise ValueError("El nombre de la asignatura debe tener al menos 4 caracteres")
        if len(curso_limpio) < 3:
            raise ValueError("El campo curso debe tener al menos 3 caracteres")
        
        if ModuloRepository.get_by_codigo(codigo_limpio, include_deleted=True):
            raise ValueError(f"El código de módulo '{codigo_limpio}' ya está registrado")
            
        return ModuloRepository.create(codigo_limpio, nombre_limpio, curso_limpio)
    
    @staticmethod
    def modificar_modulo(codigo_modulo, nuevo_nombre, nuevo_curso, rol_usuario, is_deleted=None):
        """
        Modifica un módulo existente tras validar los parámetros y el rol.
        
        Args:
            codigo_modulo (str): Código del módulo a editar.
            nuevo_nombre (str): Nuevo nombre del módulo.
            nuevo_curso (str): Nuevo curso del módulo.
            rol_usuario (str): Rol del usuario que realiza la acción.
            is_deleted (bool, optional): Estado de borrado lógico.
            
        Returns:
            Modulo: El objeto del módulo actualizado.
        """
        if rol_usuario not in ['PROFESOR', 'ADMINISTRADOR']:
            raise ValueError("Acceso denegado: Solo los profesores y administradores pueden modificar módulos")

        if not codigo_modulo:
            raise ValueError("El código del módulo es obligatorio para editarlo")
            
        codigo_limpio = codigo_modulo.strip().upper()
        modulo_existente = ModuloRepository.get_by_codigo(codigo_limpio, include_deleted=True)
        if not modulo_existente:
            raise ValueError(f"No se puede modificar: el módulo '{codigo_limpio}' no existe")
            
        nombre_limpio = modulo_existente.nombre_asignatura
        if nuevo_nombre is not None:
            nombre_limpio = nuevo_nombre.strip()
            if len(nombre_limpio) < 4:
                raise ValueError("El nuevo nombre de la asignatura debe tener al menos 4 caracteres")

        curso_limpio = modulo_existente.curso_modulo
        if nuevo_curso is not None:
            curso_limpio = nuevo_curso.strip()
            
        return ModuloRepository.update(codigo_limpio, nombre_limpio, curso_limpio, is_deleted)

    @staticmethod
    def eliminar_modulo_existente(codigo_modulo, rol_usuario):
        """
        Elimina un módulo del sistema tras comprobar los permisos.
        
        Args:
            codigo_modulo (str): Código del módulo a eliminar.
            rol_usuario (str): Rol del usuario que realiza la acción.
            
        Returns:
            bool: True si la eliminación fue exitosa.
        """
        if rol_usuario not in ['PROFESOR', 'ADMINISTRADOR']:
            raise ValueError("Acceso denegado: Solo los profesores y administradores pueden eliminar módulos")

        if not codigo_modulo:
            raise ValueError("El código del módulo es obligatorio para proceder a su eliminación")
            
        codigo_limpio = codigo_modulo.strip().upper()
        
        if not ModuloRepository.get_by_codigo(codigo_limpio, include_deleted=True):
            raise ValueError(f"No se puede eliminar: el módulo '{codigo_limpio}' no existe")
            
        return ModuloRepository.delete(codigo_limpio)