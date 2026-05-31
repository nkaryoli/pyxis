from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Base class para todos los modelos
Base = declarative_base()

# Variables globales para engine y Session
engine = None
Session = None


def init_db(database_url):
    """
    Inicializa la conexión a la base de datos.
    
    Args:
        database_url: URL de conexión a la base de datos
            Formato: mysql+pymysql://usuario:contraseña@host/base_datos
    """
    global engine, Session
    
    # Crear el engine con la URL de la BD
    engine = create_engine(database_url, echo=False)
    
    # Crear la sesión
    Session = sessionmaker(bind=engine)
    
    # NOTA: No usamos create_all() porque causa circular imports.
    # El esquema de BD ya existe (ver sql/BBDD.sql)
    # Esta línea solo verifica que la conexión sea válida
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Conexión a base de datos exitosa")
    except Exception as e:
        print(f"✗ Error de conexión: {e}")


def get_session():
    """Obtiene una nueva sesión de la base de datos."""
    if Session is None:
        raise RuntimeError("Base de datos no inicializada. Llama a init_db() primero.")
    return Session()


def should_include_deleted():
    """Retorna True si el usuario actual en el contexto HTTP es un ADMINISTRADOR."""
    from flask import has_request_context, g
    if has_request_context():
        usuario = getattr(g, 'current_user', None)
        if usuario and getattr(usuario, 'rol', None) == 'ADMINISTRADOR':
            return True
    return False