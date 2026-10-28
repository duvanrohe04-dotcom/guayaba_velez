"""
Copia de seguridad de la base SQLite antes de cada arranque.

Se ejecuta desde entrypoint.sh ANTES de seed.py. Guarda una copia consistente
(API de backup de SQLite, segura aunque la base esté en uso) en
<carpeta de la base>/backups/ y conserva solo las últimas MAX_COPIAS.
Las copias viven en el mismo volumen que la base, así que sobreviven a los
redeploys. Nunca borra ni modifica la base original; si algo falla, solo avisa.
"""
import os
import sqlite3
import sys
from datetime import datetime

MAX_COPIAS = 10


def ruta_base():
    url = os.environ.get('DATABASE_URL', '')
    if not url.startswith('sqlite:///'):
        return None
    ruta = url[len('sqlite:///'):]
    # sqlite:////abs/ruta -> /abs/ruta ; sqlite:///rel/ruta -> rel/ruta
    return ruta


def main():
    ruta = ruta_base()
    if not ruta or not os.path.isfile(ruta) or os.path.getsize(ruta) == 0:
        print('[backup] No hay base previa que respaldar (primer arranque o no es SQLite).')
        return 0

    carpeta = os.path.join(os.path.dirname(os.path.abspath(ruta)), 'backups')
    os.makedirs(carpeta, exist_ok=True)
    destino = os.path.join(carpeta, 'guayaba-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.db')

    origen = sqlite3.connect(f'file:{ruta}?mode=ro', uri=True)
    copia = sqlite3.connect(destino)
    try:
        origen.backup(copia)
    finally:
        copia.close()
        origen.close()
    print(f'[backup] Copia creada: {destino}')

    copias = sorted(f for f in os.listdir(carpeta) if f.startswith('guayaba-') and f.endswith('.db'))
    for viejo in copias[:-MAX_COPIAS]:
        os.remove(os.path.join(carpeta, viejo))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:  # un respaldo fallido nunca debe impedir el arranque
        print(f'[backup] Aviso: no se pudo respaldar ({e}). Se continúa.')
        sys.exit(0)
