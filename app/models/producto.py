from app.extensions import db


class Producto(db.Model):
    """
    Producto que se muestra en la sección "Nuestros productos" del sitio.
    El administrador los agrega, edita, oculta y elimina desde el panel.
    Sin precio a propósito: los pedidos se coordinan por WhatsApp.
    """

    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False, default='')
    # Etiquetas separadas por coma: "Natural, Tradicional, Empacada en hoja"
    etiquetas = db.Column(db.String(300), nullable=False, default='')
    cinta = db.Column(db.String(60), nullable=True)           # rótulo sobre la foto
    # Ruta relativa a /static: 'img/productos/x.jpg' (incluidos) o 'uploads/x.jpg' (subidos)
    imagen = db.Column(db.String(255), nullable=True)
    orden = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def lista_etiquetas(self):
        return [t.strip() for t in (self.etiquetas or '').split(',') if t.strip()][:6]

    @property
    def imagen_subida(self):
        """True si la foto vive en la carpeta de uploads (y por tanto se puede borrar)."""
        return bool(self.imagen) and self.imagen.startswith('uploads/')

    def __repr__(self):
        return f'<Producto {self.nombre}>'
