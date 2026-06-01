from src.extensions import get_session
from src.models.modulo import Modulo
from src.models.post import Post
from sqlalchemy import func

class ModuloRepository:
    """Repositorio para operaciones CRUD de Modulo en la BD."""

    _ICONOS_POR_MODULO = {
        "MOD-BBDD": "database",
        "MOD-PROG": "code",
        "MOD-LMAR": "file-text",
        "MOD-ENT": "spark",
        "MOD-ING": "layout",
        "MOD-TUT": "monitor",
        "MOD-DWES": "server",
        "MOD-IPO": "briefcase",
        "MOD-SIST": "shield",
        
        "MOD-SOST": "spark",
        "MOD-DIGI": "monitor",
        "MOD-ING": "layout",
        "MOD-XARX": "shield",
        "MOD-IAW": "rocket",
        "MOD-ISO": "server",
        "MOD-ASGD": "file-text",
    }

    @staticmethod
    def _asignar_icono(modulo):
        """Asigna un icono visual al módulo según su código."""
        icono = ModuloRepository._ICONOS_POR_MODULO.get(modulo.codigo_modulo, "star")
        setattr(modulo, "icono", icono)
        return modulo

    @staticmethod
    def get_all(include_deleted=False):
        """
        Obtiene todos los modulos de la BD (Todos los Usuarios).
        
        Args:
            include_deleted (bool): Si es True, incluye módulos marcados como eliminados lógicamente.

        Returns:
            list[Modulo]: Lista de módulos con los atributos dinámicos:
                - posts_count: número de posts asociados.
                - numero_posts: alias de compatibilidad para plantillas.
        """
        session = get_session()
        try:
            # Hacemos una consulta con LEFT OUTER JOIN para obtener el número de posts
            # por cada módulo en la misma consulta y evitar N+1 queries.
            query = (
                session.query(Modulo, func.count(Post.id_post).label('posts_count'))
                .outerjoin(Post, Modulo.codigo_modulo == Post.codigo_modulo)
            )
            if not include_deleted:
                query = query.filter(Modulo.is_deleted == False)
            rows = query.group_by(Modulo.codigo_modulo).all()

            modulos = []
            for modulo, posts_count in rows:
                # Anexamos atributos dinámicos para compatibilidad con plantillas
                count = int(posts_count or 0)
                setattr(modulo, 'posts_count', count)
                # Algunas plantillas o servicios usan `numero_posts`; mantenemos ambos
                setattr(modulo, 'numero_posts', count)
                modulos.append(ModuloRepository._asignar_icono(modulo))

            session.expunge_all()
            return modulos
        finally:
            session.close()

    @staticmethod
    def get_by_codigo(codigo_modulo, include_deleted=False):
        """Obtiene un modulo en especifico de la BD (Todos los Usuarios)."""
        session = get_session()
        try:
            query = session.query(Modulo).filter_by(codigo_modulo=codigo_modulo)
            if not include_deleted:
                query = query.filter_by(is_deleted=False)
            return query.first()
        finally:
            session.close()

    @staticmethod
    def get_by_name(nombre_modulo, include_deleted=False):
        """Busca un módulo por nombre ignorando mayúsculas/minúsculas."""
        session = get_session()
        try:
            query = session.query(Modulo).filter(
                func.lower(Modulo.nombre_asignatura) == nombre_modulo.lower()
            )
            if not include_deleted:
                query = query.filter(Modulo.is_deleted == False)
            return query.first()
        finally:
            session.close()

    @staticmethod
    def create(codigo_modulo, nombre_asignatura, curso_modulo):
        """Crea un nuevo modulo en la BD (Solo profesores y administradores)."""
        session = get_session()
        try:
            nuevo_modulo = Modulo(
                codigo_modulo=codigo_modulo,
                nombre_asignatura=nombre_asignatura,
                curso_modulo=curso_modulo
            )
            session.add(nuevo_modulo)
            session.commit()
            session.refresh(nuevo_modulo)
            return nuevo_modulo
        finally:
            session.close()

    @staticmethod
    def update(codigo_modulo, nuevo_nombre, nuevo_curso, is_deleted=None):
        """Actualiza un modulo existente en la BD (Solo profesores y administradores)."""
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(codigo_modulo=codigo_modulo).first()
            if modulo:
                modulo.nombre_asignatura = nuevo_nombre
                modulo.curso_modulo = nuevo_curso
                if is_deleted is not None:
                    modulo.is_deleted = is_deleted
                session.commit()
                session.refresh(modulo)
                return modulo
        finally:
            session.close()
    
    @staticmethod
    def delete(codigo_modulo):
        """Desactiva un modulo de la BD (borrado lógico)."""
        session = get_session()
        try:
            modulo = session.query(Modulo).filter_by(codigo_modulo=codigo_modulo).first()
            if modulo:
                modulo.is_deleted = True
                session.commit()
                return True
            return False
        finally:
            session.close()
