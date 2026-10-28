import os

from flask import render_template, redirect, url_for, jsonify, current_app

from app.public import public_bp
from app.models import Empresa, Contenido

_MIME = {
    'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
    'gif': 'image/gif', 'webp': 'image/webp', 'svg': 'image/svg+xml',
}


def _logo_vigente():
    """(ruta estática, mime) del logo del panel, o del provisional si no hay."""
    empresa = Empresa.get_instance()
    archivo = (
        'uploads/' + empresa.logo_filename if empresa.logo_filename
        else 'img/logo-placeholder.svg'
    )
    ext = archivo.rsplit('.', 1)[-1].lower()
    return archivo, _MIME.get(ext, 'image/png')


@public_bp.route('/')
def index():
    empresa = Empresa.get_instance()
    secciones = {c.seccion: c for c in Contenido.query.order_by(Contenido.orden).all()}
    return render_template('public/index.html', empresa=empresa, secciones=secciones)


@public_bp.route('/favicon.ico')
def favicon():
    """Los navegadores piden /favicon.ico: se redirige al logo del panel."""
    archivo, _ = _logo_vigente()
    return redirect(url_for('static', filename=archivo), code=302)


@public_bp.route('/manifest.webmanifest')
def manifest():
    """Permite instalar el sitio como app / acceso directo con el logo del panel."""
    empresa = Empresa.get_instance()
    archivo, mime = _logo_vigente()
    icono = url_for('static', filename=archivo)
    datos = {
        'name': empresa.nombre,
        'short_name': empresa.nombre[:12],
        'description': 'Guayaba Veleña de la vereda Guayabal, Vélez, Santander. Producción sostenible.',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'background_color': '#fdf8f2',
        'theme_color': '#2d5a27',
        'lang': 'es',
        'icons': [
            {'src': icono, 'sizes': 'any', 'type': mime, 'purpose': 'any'},
            {'src': icono, 'sizes': '512x512', 'type': mime, 'purpose': 'maskable'},
        ],
    }
    resp = jsonify(datos)
    resp.headers['Content-Type'] = 'application/manifest+json'
    resp.headers['Cache-Control'] = 'no-cache'
    return resp


@public_bp.route('/healthz')
def healthz():
    """Sonda de vida para Docker/Coolify. No toca la base de datos."""
    return {'status': 'ok'}, 200
