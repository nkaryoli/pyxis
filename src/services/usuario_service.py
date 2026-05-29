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
        res = UsuarioService.obtener_usuario_por_id(id_usuario)
        usuario = res[0] if isinstance(res, tuple) else res
        return usuario.tokens

    @staticmethod
    def actualizar_usuario(id_usuario_destino, datos, usuario_id_solicitante):
        """
        Actualiza los datos de un usuario existente aplicando permisos avanzados.

        Esta función controla los cambios permitidos según el rol del usuario solicitante, 
        valida la integridad y dominios autorizados de correos electrónicos, y realiza 
        recalculación automática del nombre de usuario si cambian las direcciones de email.

        Args:
            id_usuario_destino (int): ID del usuario a modificar.
            datos (dict): Diccionario con los campos clave-valor a actualizar.
            usuario_id_solicitante (int/str): ID del usuario que inicia la actualización.

        Raises:
            ValueError: Si el rol es ALUMNO y trata de modificar a otro usuario.
            ValueError: Si el email no pertenece a los dominios autorizados (@monlau.com, @campus.monlau.com, @pixys.com).
            ValueError: Si el nuevo email ya está registrado en el sistema.
            ValueError: Si no se provee ningún parámetro válido a modificar.

        Returns:
            Usuario: Objeto del usuario actualizado en base de datos.
        """
        print('el id del solicitante es ', usuario_id_solicitante)
        print('el id del destino es ', id_usuario_destino)
        
        solicitante_res = UsuarioService.obtener_usuario_por_id(usuario_id_solicitante)
        destino_res = UsuarioService.obtener_usuario_por_id(id_usuario_destino)
        
        solicitante = solicitante_res[0] if isinstance(solicitante_res, tuple) else solicitante_res
        destino = destino_res[0] if isinstance(destino_res, tuple) else destino_res

        datos_filtrados = {}

        if solicitante.rol == 'ALUMNO':
            if int(id_usuario_destino) != int(usuario_id_solicitante):
                raise ValueError("Un alumno no puede editar los datos de otros usuarios.")
            
            elif int(id_usuario_destino) == int(usuario_id_solicitante) and 'imagen_usuario' in datos:
                datos_filtrados['imagen_usuario'] = datos['imagen_usuario']
                print("Datos a actualizar:", datos_filtrados)

        elif solicitante.rol in ['PROFESOR', 'ADMINISTRADOR']:           
            campos_prohibidos = ['id_usuario', 'fecha_alta', 'password_usuario']
            datos_filtrados = {k: v for k, v in datos.items() if k not in campos_prohibidos}                
            
            nuevo_email = datos_filtrados.get('email_usuario')
            if nuevo_email and nuevo_email != destino.email_usuario:
                nuevo_email_lower = nuevo_email.strip().lower()
                dominios_validos = ('@monlau.com', '@campus.monlau.com', '@pixys.com')
                if not any(nuevo_email_lower.endswith(dom) for dom in dominios_validos):
                    raise ValueError("El email debe pertenecer a un dominio autorizado.")
                
                if UsuarioRepository.get_by_email(nuevo_email_lower):
                    raise ValueError("El nuevo email ya está en uso por otro usuario.")
                
                datos_filtrados['email_usuario'] = nuevo_email_lower
                parte_local = nuevo_email_lower.split('@', 1)[0]
                datos_filtrados['username'] = parte_local[:-6] if len(parte_local) > 6 else parte_local            
        
        if not datos_filtrados:
            raise ValueError("No se han proporcionado datos válidos para actualizar.")
            
        return UsuarioRepository.update(id_usuario_destino, datos_filtrados)

    @staticmethod
    def eliminar_usuario(id_usuario, usuario_rol):
        """Lógica para eliminar un usuario."""               
        
        if usuario_rol != 'ADMINISTRADOR':
            raise ValueError("No se puede eliminar a un usuario si no eres administrador.")
            
        return UsuarioRepository.delete(id_usuario)
    
    
    @staticmethod
    def obtener_posts_paginados(id_usuario, page=1, per_page=ITEMS_PER_PAGE):
        """
        Obtiene de manera paginada el listado de posts creados por un usuario concreto.

        Args:
            id_usuario (int): ID del usuario propietario de los posts.
            page (int): Número de la página de resultados a consultar. Por defecto 1.
            per_page (int): Cantidad de elementos por página.

        Returns:
            tuple: (items_dict, total_pages)
                - items_dict (list): Listado de posts en formato diccionario con metadatos asociados.
                - total_pages (int): Cantidad total de páginas de resultados disponibles.
        """
        offset = (page - 1) * per_page
        items = PostRepository.get_by_user_paginated(id_usuario, limit=per_page, offset=offset)
        total_count = PostRepository.count_by_user(id_usuario)
        
        total_pages = max(1, ceil(total_count / per_page))
        
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
        """
        Obtiene de manera paginada las respuestas registradas por un usuario concreto.

        Args:
            id_usuario (int): ID del usuario creador de las respuestas.
            page (int): Número de la página de resultados a consultar. Por defecto 1.
            per_page (int): Cantidad de elementos por página.

        Returns:
            tuple: (items_dict, total_pages)
                - items_dict (list): Listado de respuestas mapeadas a diccionarios.
                - total_pages (int): Cantidad total de páginas de resultados disponibles.
        """
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
        """
        Obtiene las notificaciones pendientes de respuestas recibidas en los posts del usuario.

        Las respuestas recibidas de otros usuarios en los posts del usuario especificado se
        ordenan cronológicamente de manera descendente y se devuelven paginadas.

        Args:
            id_usuario (int): ID del usuario para el cual obtener notificaciones.
            page (int): Número de la página de resultados a consultar. Por defecto 1.
            per_page (int): Cantidad de elementos por página.

        Returns:
            tuple: (notificaciones_paginadas, total_pages)
                - notificaciones_paginadas (list): Listado de notificaciones para la página actual.
                - total_pages (int): Cantidad total de páginas de resultados disponibles.
        """
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
    
    
    