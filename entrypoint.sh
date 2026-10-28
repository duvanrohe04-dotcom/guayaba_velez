#!/bin/sh
# Respalda la base, la inicializa (idempotente) y luego arranca el servidor.
# seed.py solo crea lo que falta: admin, fila de empresa y secciones de texto.
# NUNCA borra ni sobrescribe datos existentes.
set -e

echo "[entrypoint] Respaldando la base de datos (si existe)..."
python backup_db.py || true

echo "[entrypoint] Inicializando base de datos y datos base..."
python seed.py

echo "[entrypoint] Arrancando: $*"
exec "$@"
