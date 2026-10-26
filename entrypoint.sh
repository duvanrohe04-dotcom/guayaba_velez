#!/bin/sh
# Inicializa la base de datos (idempotente) y luego arranca el servidor.
# seed.py solo crea lo que falta: admin, fila de empresa y secciones de texto.
set -e

echo "[entrypoint] Inicializando base de datos y datos base..."
python seed.py

echo "[entrypoint] Arrancando: $*"
exec "$@"
