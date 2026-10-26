import os
from datetime import datetime, timezone

from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.admin import admin_bp
from app.admin.forms import EmpresaForm, ContenidoForm, CuentaForm
from app.extensions import db
from app.models import Empresa, Contenido, Usuario


def _allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in current_app.config['ALLOWED_EXTENSIONS']


def _borrar_logo_anterior(nombre):
    """Elimina el logo que quedó reemplazado, para no acumular archivos.

    Se borra solo tras el commit: si la transacción falla, el archivo viejo
    sigue en disco y la BD sigue apuntando a él. La ruta se resuelve y se
    compara contra la carpeta de uploads para no poder borrar nada de
    fuera (por ejemplo si el nombre viniera con '..').
    """
    if not nombre:
        return
    carpeta = os.path.realpath(current_app.config['UPLOAD_FOLDER'])
    ruta = os.path.realpath(os.path.join(carpeta, os.path.basename(nombre)))
    if os.path.dirname(ruta) != carpeta:
        return
    try:
        os.remove(ruta)
    except OSError:
        pass  # si ya no existe, no es un problema


# Ruta '' + url_prefix '/admin' = exactamente /admin, sin barra final.
# strict_slashes=False hace que /admin/ tambien funcione.
@admin_bp.route('', strict_slashes=False)
@login_required
def dashboard():
    empresa = Empresa.get_instance()
    secciones = Contenido.query.order_by(Contenido.orden).all()
    return render_template('admin/dashboard.html', empresa=empresa, secciones=secciones)


@admin_bp.route('/empresa', methods=['GET', 'POST'])
@login_required
def editar_empresa():
    empresa = Empresa.get_instance()
    form = EmpresaForm(obj=empresa)

    if form.validate_on_submit():
        empresa.nombre = form.nombre.data or empresa.nombre
        empresa.whatsapp = form.whatsapp.data
        empresa.facebook = form.facebook.data
        empresa.instagram = form.instagram.data
        empresa.tiktok = form.tiktok.data

        logo_anterior = empresa.logo_filename
        logo_nuevo = None

        archivo = form.logo.data
        if archivo and _allowed_file(archivo.filename):
            ext = archivo.filename.rsplit('.', 1)[-1].lower()
            # now(timezone.utc) es aware; utcnow() estaba deprecado y ademas
            # su .timestamp() interpretaba la hora como local, no como UTC.
            marca = datetime.now(timezone.utc).timestamp()
            nombre_archivo = secure_filename(f"logo_{marca:.0f}.{ext}")
            ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_archivo)
            archivo.save(ruta)
            empresa.logo_filename = nombre_archivo
            logo_nuevo = nombre_archivo

        db.session.commit()

        # Solo se borra el anterior si de verdad se substituyo por otro.
        # Si en este guardado no se subio logo, el archivo vigente sigue en uso.
        if logo_nuevo and logo_anterior and logo_anterior != logo_nuevo:
            _borrar_logo_anterior(logo_anterior)

        flash('Datos de la empresa actualizados.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/editar_empresa.html', form=form, empresa=empresa)


@admin_bp.route('/contenido/<seccion>', methods=['GET', 'POST'])
@login_required
def editar_contenido(seccion):
    bloque = Contenido.get_por_seccion(seccion)
    if bloque is None:
        flash('Esa sección no existe.', 'warning')
        return redirect(url_for('admin.dashboard'))

    form = ContenidoForm(obj=bloque)
    if form.validate_on_submit():
        bloque.titulo = form.titulo.data
        bloque.texto = form.texto.data
        db.session.commit()
        flash(f'Sección "{seccion}" actualizada.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/editar_contenido.html', form=form, bloque=bloque)


@admin_bp.route('/cuenta', methods=['GET', 'POST'])
@login_required
def cuenta():
    """Cambia el usuario y la contraseña de acceso al panel."""
    form = CuentaForm(username=current_user.username)

    if form.validate_on_submit():
        usuario = db.session.get(Usuario, current_user.id)

        # Se pide la contraseña actual para confirmar que quien edita es
        # el dueño de la cuenta y no alguien con la sesión abierta.
        if not usuario.check_password(form.password_actual.data):
            flash('La contraseña actual no es correcta.', 'danger')
            return redirect(url_for('admin.cuenta'))

        nuevo_usuario = form.username.data.strip()
        if nuevo_usuario != usuario.username:
            if Usuario.query.filter_by(username=nuevo_usuario).first() is not None:
                flash('Ese nombre de usuario ya está en uso.', 'danger')
                return redirect(url_for('admin.cuenta'))
            usuario.username = nuevo_usuario

        # Vacío significa "déjala como está".
        if form.password.data:
            usuario.set_password(form.password.data)

        db.session.commit()
        flash('Datos de acceso actualizados.', 'success')
        return redirect(url_for('admin.cuenta'))

    return render_template('admin/cuenta.html', form=form)
