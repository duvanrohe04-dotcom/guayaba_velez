from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='../templates/admin')

from app.auth import routes  # noqa: E402,F401  (registra las rutas en el blueprint)
