from app.extensions import db


class Empresa(db.Model):
    """
    Datos generales de la empresa mostrados en todo el sitio: logo, nombre
    y accesos directos a redes sociales. Se maneja como fila única (id=1).
    """

    __tablename__ = 'empresa'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False, default='Guayaba Veleña')
    logo_filename = db.Column(db.String(255), nullable=True)

    whatsapp = db.Column(db.String(50), nullable=True)     # solo el número, ej: 573001234567
    facebook = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    tiktok = db.Column(db.String(255), nullable=True)

    @staticmethod
    def get_instance():
        """Devuelve la única fila de configuración, creándola si no existe."""
        empresa = db.session.get(Empresa, 1)
        if empresa is None:
            empresa = Empresa(id=1)
            db.session.add(empresa)
            db.session.commit()
        return empresa

    @property
    def whatsapp_link(self):
        if not self.whatsapp:
            return None
        numero = ''.join(filter(str.isdigit, self.whatsapp))
        return f'https://wa.me/{numero}'

    def __repr__(self):
        return f'<Empresa {self.nombre}>'
