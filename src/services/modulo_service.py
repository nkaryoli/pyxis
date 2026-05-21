from src.repositories.modulo_repository import ModuloRepository

class ModuloService:
    """Servicio de lógica de negocio para la gestión de Módulos académicos."""

    @staticmethod
    def obtener_todos_los_modulos():
        """Obtiene todas las asignaturas de la base de datos."""
        return ModuloRepository.get_all()
    
    @staticmethod
    def obtener_modulo_por_codigo(codigo_modulo):
        """Busca una asignatura por su clave primaria string y valida su existencia."""
        if not codigo_modulo:
            raise ValueError("El código del módulo no puede estar vacío.")
        modulo = ModuloRepository.get_by_codigo(codigo_modulo.strip().upper())
        if not modulo:
            raise ValueError(f"Módulo con código '{codigo_modulo}' no encontrado.")
        return modulo
    
    @staticmethod
    def crear_nuevo_modulo(codigo_modulo, nombre_asignatura, curso_modulo, rol_usuario):
        """Crea un nuevo módulo con validación de campos y rol."""
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
        
        if ModuloRepository.get_by_codigo(codigo_limpio):
            raise ValueError(f"El código de módulo '{codigo_limpio}' ya está registrado")
            
        return ModuloRepository.create(codigo_limpio, nombre_limpio, curso_limpio)
    
    @staticmethod
    def modificar_modulo(codigo_modulo, nuevo_nombre, nuevo_curso, rol_usuario):
        """Modifica un módulo existente tras validar los parámetros y el rol. Acceso: Solo prof y admin."""
        if rol_usuario not in ['PROFESOR', 'ADMINISTRADOR']:
            raise ValueError("Acceso denegado: Solo los profesores y administradores pueden modificar módulos")

        if not codigo_modulo:
            raise ValueError("El código del módulo es obligatorio para editarlo")
        if not nuevo_nombre or not nuevo_curso:
            raise ValueError("Los campos modificados no pueden quedarse vacíos")
            
        codigo_limpio = codigo_modulo.strip().upper()
        nombre_limpio = nuevo_nombre.strip()
        curso_limpio = nuevo_curso.strip()
        
        if len(nombre_limpio) < 4:
            raise ValueError("El nuevo nombre de la asignatura debe tener al menos 4 caracteres")

        modulo_existente = ModuloRepository.get_by_codigo(codigo_limpio)
        if not modulo_existente:
            raise ValueError(f"No se puede modificar: el módulo '{codigo_limpio}' no existe")
            
        return ModuloRepository.update(codigo_limpio, nombre_limpio, curso_limpio)

    @staticmethod
    def eliminar_modulo_existente(codigo_modulo, rol_usuario):
        """Elimina un módulo del sistema tras comprobar los permisos. Acceso: Solo prof y admin."""
        if rol_usuario not in ['PROFESOR', 'ADMINISTRADOR']:
            raise ValueError("Acceso denegado: Solo los profesores y administradores pueden eliminar módulos")

        if not codigo_modulo:
            raise ValueError("El código del módulo es obligatorio para proceder a su eliminación")
            
        codigo_limpio = codigo_modulo.strip().upper()
        
        if not ModuloRepository.get_by_codigo(codigo_limpio):
            raise ValueError(f"No se puede eliminar: el módulo '{codigo_limpio}' no existe")
            
        return ModuloRepository.delete(codigo_limpio)