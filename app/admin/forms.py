from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, EqualTo, NumberRange


class EmpresaForm(FlaskForm):
    nombre = StringField('Nombre de la empresa', validators=[Length(max=150)])
    logo = FileField(
        'Logo',
        validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'webp'], 'Solo se permiten imágenes.')]
    )
    whatsapp = StringField('WhatsApp (con indicativo, ej: 573001234567)', validators=[Optional(), Length(max=50)])
    facebook = StringField('Enlace de Facebook', validators=[Optional(), Length(max=255)])
    instagram = StringField('Enlace de Instagram', validators=[Optional(), Length(max=255)])
    tiktok = StringField('Enlace de TikTok', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Guardar cambios')


class ContenidoForm(FlaskForm):
    titulo = StringField('Título de la sección', validators=[Optional(), Length(max=200)])
    texto = TextAreaField('Texto', validators=[Optional()])
    submit = SubmitField('Guardar sección')


class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del producto', validators=[DataRequired(message='Escribe el nombre.'), Length(max=150)])
    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=600)])
    etiquetas = StringField(
        'Etiquetas (separadas por coma)',
        validators=[Optional(), Length(max=300)],
        render_kw={'placeholder': 'Natural, Tradicional, Empacada en calceta de plátano'},
    )
    cinta = StringField(
        'Rótulo sobre la foto (opcional)',
        validators=[Optional(), Length(max=60)],
        render_kw={'placeholder': 'Producto tradicional'},
    )
    imagen = FileField(
        'Foto del producto',
        validators=[FileAllowed(['png', 'jpg', 'jpeg', 'webp', 'gif'], 'Solo se permiten imágenes.')]
    )
    orden = IntegerField('Posición en la lista (1 = primero)', validators=[Optional(), NumberRange(min=0, max=999)], default=0)
    activo = BooleanField('Mostrar en el sitio', default=True)
    submit = SubmitField('Guardar producto')


class AccionForm(FlaskForm):
    """Formulario vacío: solo aporta el token CSRF a los botones de eliminar / ocultar."""


class CuentaForm(FlaskForm):
    """Cambio de credenciales de acceso al panel."""

    password_actual = PasswordField(
        'Contraseña actual',
        validators=[DataRequired()],
        render_kw={'autocomplete': 'current-password'},
    )
    username = StringField(
        'Usuario',
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={'autocomplete': 'username'},
    )
    password = PasswordField(
        'Nueva contraseña',
        validators=[Optional(), Length(min=8, max=128)],
        render_kw={'autocomplete': 'new-password'},
    )
    confirmar_password = PasswordField(
        'Repite la nueva contraseña',
        validators=[EqualTo('password', message='Las contraseñas no coinciden.')],
        render_kw={'autocomplete': 'new-password'},
    )
    submit = SubmitField('Guardar cambios')
