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
    def whatsapp_numero(self):
        """
        Número listo para wa.me: solo dígitos y con indicativo de país.
        Acepta '+57 300 123 4567', '(57) 300-123-4567', '573001234567' o el
        celular colombiano sin indicativo ('300 123 4567' -> '573001234567').
        Devuelve None si no hay un número usable.
        """
        digitos = ''.join(filter(str.isdigit, self.whatsapp or ''))
        if digitos.startswith('00'):
            digitos = digitos[2:]
        if len(digitos) == 10 and digitos.startswith('3'):   # celular de Colombia sin 57
            digitos = '57' + digitos
        return digitos if len(digitos) >= 11 else None

    @property
    def whatsapp_link(self):
        numero = self.whatsapp_numero
        return f'https://wa.me/{numero}' if numero else None

    def __repr__(self):
        return f'<Empresa {self.nombre}>'
