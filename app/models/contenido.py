from app.extensions import db


class Contenido(db.Model):
    """
    Bloques de texto editables del sitio público, identificados por una
    clave única ('seccion'). Permite que el admin edite textos sin tocar código.
    """

    __tablename__ = 'contenido'

    id = db.Column(db.Integer, primary_key=True)
    seccion = db.Column(db.String(80), unique=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=True)
    texto = db.Column(db.Text, nullable=False, default='')
    orden = db.Column(db.Integer, nullable=False, default=0)

    @staticmethod
    def get_por_seccion(seccion):
        return Contenido.query.filter_by(seccion=seccion).first()

    def __repr__(self):
        return f'<Contenido {self.seccion}>'
