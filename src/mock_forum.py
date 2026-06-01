from datetime import datetime, timedelta
import unicodedata


MODULES = [
	{
		"codigo_modulo": "PROG",
		"nombre_asignatura": "Programación",
		"curso_modulo": "1º DAM",
	},
	{
		"codigo_modulo": "LM",
		"nombre_asignatura": "Lenguaje de Marcas",
		"curso_modulo": "1º DAM",
	},
	{
		"codigo_modulo": "BBDD",
		"nombre_asignatura": "Bases de Datos",
		"curso_modulo": "1º DAM",
	},
	{
		"codigo_modulo": "ED",
		"nombre_asignatura": "Entornos de Desarrollo",
		"curso_modulo": "1º DAM",
	},
	{
		"codigo_modulo": "SI",
		"nombre_asignatura": "Sistemas Informáticos",
		"curso_modulo": "1º DAM",
	},
]


NOW = datetime(2026, 5, 25, 12, 0)


def slugify(value):
	texto = (value or "").strip().lower()
	texto = unicodedata.normalize('NFKD', texto)
	texto = ''.join(char for char in texto if not unicodedata.combining(char))
	texto = texto.replace('&', ' y ')
	texto = ''.join(char if char.isalnum() else '-' for char in texto)
	while '--' in texto:
		texto = texto.replace('--', '-')
	return texto.strip('-')


POSTS = [
	{
		"id_post": 1,
		"titulo_post": "¿Cuándo usar INNER JOIN y cuándo LEFT JOIN?",
		"contenido_post": "Tengo dudas sobre qué tablas se pierden en cada tipo de join y cómo se explica en un examen.",
		"codigo_modulo": "BBDD",
		"modulo_nombre": "Bases de Datos",
		"curso_modulo": "1º DAM",
		"autor": "Barkå",
		"created_at": NOW - timedelta(hours=2),
		"destacado": True,
		"respuestas_count": 3,
		"respuestas": [
			{"autor": "Menelwie", "contenido": "INNER devuelve coincidencias. LEFT conserva la fila izquierda aunque no haya match.", "created_at": NOW - timedelta(hours=1, minutes=30), "mejor": True},
			{"autor": "Ricote", "contenido": "Haz una tabla de verdad con tres filas y lo verás más claro.", "created_at": NOW - timedelta(hours=1, minutes=5), "mejor": False},
		],
	},
	{
		"id_post": 2,
		"titulo_post": "¿Cómo estructurar mejor un HTML con Jinja?",
		"contenido_post": "Me pierdo entre base, bloques y partials. Quiero una estructura limpia para el proyecto.",
		"codigo_modulo": "LM",
		"modulo_nombre": "Lenguaje de Marcas",
		"curso_modulo": "1º DAM",
		"autor": "Belter",
		"created_at": NOW - timedelta(hours=4),
		"destacado": True,
		"respuestas_count": 4,
		"respuestas": [
			{"autor": "Brittany", "contenido": "Piensa en base + bloques + componentes reutilizables. No metas todo en una sola plantilla.", "created_at": NOW - timedelta(hours=3, minutes=40), "mejor": True},
		],
	},
	{
		"id_post": 3,
		"titulo_post": "¿Qué validaciones mínimas debería hacer el login?",
		"contenido_post": "Estoy montando el formulario y no sé si validar solo en servidor o también en frontend.",
		"codigo_modulo": "PROG",
		"modulo_nombre": "Programación",
		"curso_modulo": "1º DAM",
		"autor": "Lothar",
		"created_at": NOW - timedelta(days=1, hours=2),
		"destacado": False,
		"respuestas_count": 2,
		"respuestas": [
			{"autor": "Kaivax", "contenido": "Siempre valida en backend. En frontend añade UX para evitar errores tontos.", "created_at": NOW - timedelta(days=1, hours=1, minutes=20), "mejor": True},
		],
	},
	{
		"id_post": 4,
		"titulo_post": "¿Cómo organizar la carpeta static en Flask?",
		"contenido_post": "Quiero separar CSS, JS y assets sin perderme con las rutas.",
		"codigo_modulo": "ED",
		"modulo_nombre": "Entornos de Desarrollo",
		"curso_modulo": "1º DAM",
		"autor": "Arendelium",
		"created_at": NOW - timedelta(days=1, hours=4),
		"destacado": False,
		"respuestas_count": 1,
		"respuestas": [
			{"autor": "Neosaro", "contenido": "Separa por css, js, images y usa url_for para no hardcodear rutas.", "created_at": NOW - timedelta(days=1, hours=3, minutes=30), "mejor": True},
		],
	},
	{
		"id_post": 5,
		"titulo_post": "¿Qué índices usaría en una tabla de posts?",
		"contenido_post": "Tengo filtros por módulo, fecha y autor, y no sé por dónde empezar.",
		"codigo_modulo": "BBDD",
		"modulo_nombre": "Bases de Datos",
		"curso_modulo": "1º DAM",
		"autor": "Ricote",
		"created_at": NOW - timedelta(hours=8),
		"destacado": True,
		"respuestas_count": 5,
		"respuestas": [
			{"autor": "Kaivax", "contenido": "Si filtras por módulo y fecha, indexa primero lo más selectivo.", "created_at": NOW - timedelta(hours=7, minutes=40), "mejor": True},
		],
	},
	{
		"id_post": 6,
		"titulo_post": "¿Cómo organizar el navbar para la app?",
		"contenido_post": "Estoy diseñando la navegación y no sé qué secciones deben ir fijas arriba.",
		"codigo_modulo": "LM",
		"modulo_nombre": "Lenguaje de Marcas",
		"curso_modulo": "1º DAM",
		"autor": "Brittany",
		"created_at": NOW - timedelta(hours=12),
		"destacado": False,
		"respuestas_count": 2,
		"respuestas": [
			{"autor": "Menelwie", "contenido": "Pon módulos, destacados y recientes. El resto mejor en páginas secundarias.", "created_at": NOW - timedelta(hours=11, minutes=15), "mejor": True},
		],
	},
]


def get_modules():
	modules = []
	for module in MODULES:
		posts_count = len([post for post in POSTS if post["codigo_modulo"] == module["codigo_modulo"]])
		modules.append({**module, "posts_count": posts_count, "nombre_slug": slugify(module["nombre_asignatura"])})
	return modules


def get_module_by_code(codigo_modulo):
	codigo_limpio = (codigo_modulo or "").strip().upper()
	for module in get_modules():
		if module["codigo_modulo"] == codigo_limpio:
			return module
	return None


def get_module_by_slug(nombre_slug):
	slug_limpio = slugify(nombre_slug)
	for module in get_modules():
		if module["nombre_slug"] == slug_limpio:
			return module
	return None


def get_posts():
	posts = []
	for post in POSTS:
		posts.append({**post, "modulo_slug": slugify(post["modulo_nombre"])})
	return sorted(posts, key=lambda post: post["created_at"], reverse=True)


def get_posts_by_module(codigo_modulo):
	codigo_limpio = (codigo_modulo or "").strip().upper()
	return [post for post in get_posts() if post["codigo_modulo"] == codigo_limpio]


def get_post_by_id(id_post):
	for post in get_posts():
		if post["id_post"] == id_post:
			return post
	return None


def get_featured_posts():
	return [post for post in get_posts() if post["destacado"]]


def get_recent_posts():
	return get_posts()