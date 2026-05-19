from sqlalchemy import create_engine
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
    
    # Crear todas las tablas definidas en los modelos
    Base.metadata.create_all(engine)


def get_session():
    """Obtiene una nueva sesión de la base de datos."""
    if Session is None:
        raise RuntimeError("Base de datos no inicializada. Llama a init_db() primero.")
    return Session()