import os
from dotenv import load_dotenv
load_dotenv()

def _bool(env_value, default=False):
    if env_value is None:
        return default
    return str(env_value).lower() in ('1', 'true', 'yes', 'on')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # En prod debe ser obligatoria
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'abptest')

    # Cookie security flags (se leen desde env y se convierten correctamente)
    SESSION_COOKIE_SECURE = _bool(os.environ.get('SESSION_COOKIE_SECURE'), False)
    SESSION_COOKIE_HTTPONLY = _bool(os.environ.get('SESSION_COOKIE_HTTPONLY'), True)
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    REMEMBER_COOKIE_SECURE = _bool(os.environ.get('REMEMBER_COOKIE_SECURE'), False)