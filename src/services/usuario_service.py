from src.repositories.usuario_repository import UsuarioRepository
from src.services.post_service import PostService
from src.repositories.respuesta_repository import RespuestaRepository
from src.repositories.post_repository import PostRepository
from src.repositories.matricula_repository import MatriculaRepository
from math import ceil

ITEMS_PER_PAGE = 5

class UsuarioService:
    """Servicio de lógica de negocio para la gestión de Usuarios."""

    @staticmethod
    def obtener_todos_los_usuarios():
        """Devuelve todos los usuarios para vistas de administración."""
        return UsuarioRepository.get_all()

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
            posts = []        
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
    
    
    @staticmethod
    def obtener_posts_paginados(id_usuario, page=1, per_page=ITEMS_PER_PAGE):
        # 1. Obtener el repositorio (ajusta según tu estructura)
        # Suponiendo que tienes un PostRepository que puede filtrar
        offset = (page - 1) * per_page
        
        # Obtener items y el total para calcular páginas
        items = PostRepository.get_by_user_paginated(id_usuario, limit=per_page, offset=offset)
        total_count = PostRepository.count_by_user(id_usuario)
        
        total_pages = max(1, ceil(total_count / per_page))
        
        # Convertir a formato dict si es necesario
        items_dict = []
        for r in items:
            post = PostRepository.get_by_id(r.id_post)
            dto = r.to_dict()
            dto['titulo_post'] = post.titulo_post if post else None
            dto['codigo_modulo'] = post.codigo_modulo if post else None
            items_dict.append(dto)
        
        return items_dict, total_pages

    @staticmethod
    def obtener_respuestas_paginadas(id_usuario, page=1, per_page=ITEMS_PER_PAGE):
        offset = (page - 1) * per_page
        
        items = RespuestaRepository.get_by_user_paginated(id_usuario, limit=per_page, offset=offset)
        total_count = RespuestaRepository.count_by_user(id_usuario)
        
        total_pages = max(1, ceil(total_count / per_page))
        
        items_dict = []
        for r in items:
            post = PostRepository.get_by_id(r.id_post)
            dto = r.to_dict()
            dto['titulo_post'] = post.titulo_post if post else None
            dto['codigo_modulo'] = post.codigo_modulo if post else None
            dto['usuario_respondedor'] = r.autor
            items_dict.append(dto)
        
        return items_dict, total_pages

    @staticmethod
    def obtener_notificaciones_paginadas(id_usuario, page=1, per_page=ITEMS_PER_PAGE):
        posts = PostRepository.get_by_user_id(id_usuario)
        notificaciones = []

        for post in posts:
            respuestas = RespuestaRepository.get_by_post_id(post.id_post)
            for respuesta in respuestas:
                if respuesta.id_usuario == id_usuario:
                    continue
                dto = respuesta.to_dict()
                dto['titulo_post'] = post.titulo_post
                dto['codigo_modulo'] = post.codigo_modulo
                dto['usuario_respondedor'] = respuesta.autor
                notificaciones.append(dto)

        notificaciones.sort(key=lambda x: x.get('fecha_respuesta') or '', reverse=True)
        total_count = len(notificaciones)
        total_pages = max(1, ceil(total_count / per_page))

        inicio = (page - 1) * per_page
        return notificaciones[inicio:inicio + per_page], total_pages
    
    @staticmethod
    def esta_matriculado(usuario, codigo_modulo):
        if usuario.rol in ['ADMINISTRADOR', 'PROFESOR']:
            return True
        return MatriculaRepository.verificar_matricula(usuario.id_usuario, codigo_modulo)

    @staticmethod
    def obtener_modulos_usuario(usuario):
        return MatriculaRepository.get_modulos_para_usuario(usuario)
    
    
    