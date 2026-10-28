"""Procesamiento de fotos subidas desde el panel."""
import os
import uuid

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = 50_000_000   # evita "bombas" de descompresión
LADO_MAX = 1400                       # px: sobra para una tarjeta y pesa poco


def guardar_foto_producto(archivo, carpeta):
    """
    Valida que sea una imagen real, corrige la rotación del celular, quita los
    metadatos (GPS, etc.), la reduce a LADO_MAX y la guarda como JPG.
    Devuelve la ruta relativa a /static ('uploads/xxx.jpg') o None si no es válida.
    """
    try:
        img = Image.open(archivo.stream)
        img.load()
        img = ImageOps.exif_transpose(img)
    except Exception:
        return None

    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        rgba = img.convert('RGBA')
        fondo = Image.new('RGB', rgba.size, (255, 255, 255))
        fondo.paste(rgba, mask=rgba.split()[-1])
        img = fondo
    else:
        img = img.convert('RGB')

    img.thumbnail((LADO_MAX, LADO_MAX), Image.LANCZOS)
    nombre = f'producto_{uuid.uuid4().hex[:12]}.jpg'
    os.makedirs(carpeta, exist_ok=True)
    img.save(os.path.join(carpeta, nombre), 'JPEG', quality=85, optimize=True, progressive=True)
    return f'uploads/{nombre}'


def borrar_foto_subida(ruta_relativa, carpeta):
    """Borra un archivo de uploads. Solo actúa dentro de la carpeta de uploads."""
    if not ruta_relativa or not ruta_relativa.startswith('uploads/'):
        return
    base = os.path.realpath(carpeta)
    ruta = os.path.realpath(os.path.join(base, os.path.basename(ruta_relativa)))
    if os.path.dirname(ruta) != base:
        return
    try:
        os.remove(ruta)
    except OSError:
        pass
