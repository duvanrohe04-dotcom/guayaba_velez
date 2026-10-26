"""
Punto único de importación de modelos. Importarlos aquí garantiza que
SQLAlchemy los registre antes de db.create_all(), sin importar el orden
en que los usen los blueprints.
"""
from app.models.usuario import Usuario
from app.models.empresa import Empresa
from app.models.contenido import Contenido

__all__ = ['Usuario', 'Empresa', 'Contenido']
