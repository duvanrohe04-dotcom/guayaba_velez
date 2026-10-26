import os

from dotenv import load_dotenv

# Las variables reales del sistema mandan sobre las del archivo .env,
# para que en Docker/Coolify la configuración venga del entorno.
load_dotenv(override=False)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configuración base de la aplicación, leída desde variables de entorno."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambia-esta-clave-en-produccion')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'instance', 'guayaba.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Subida de logo
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB máximo por archivo subido

    # Credenciales iniciales del admin (solo usadas por seed.py)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'cambiar123')
