import os
from flask import Flask, url_for

from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    """Application factory: crea y configura la instancia de Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.public import public_bp

    @app.context_processor
    def inyectar_marca():
        """Nombre y logo vigentes (los del panel) disponibles en todas las plantillas."""
        from app.models import Empresa
        try:
            empresa = Empresa.get_instance()
        except Exception:
            return {}
        if empresa.logo_filename:
            logo = url_for('static', filename='uploads/' + empresa.logo_filename)
        else:
            logo = url_for('static', filename='img/logo-placeholder.svg')
        return {'marca_nombre': empresa.nombre, 'marca_logo': logo}

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)

    return app
