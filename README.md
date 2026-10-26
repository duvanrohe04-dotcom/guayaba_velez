# Guayaba Veleña — sitio web

Proyecto Flask para el proceso productivo de guayaba y bocadillo veleño,
fincas Buena Vista y El Placer, vereda Guayabal, Vélez (Santander).

## Estructura

```
app/
├── models/     -> Usuario, Empresa, Contenido (SQLAlchemy)
├── auth/       -> login/logout del admin (Flask-Login)
├── admin/      -> panel privado (editar logo, nombre, redes, textos)
├── public/     -> sitio público informativo
├── templates/
└── static/
```

## Puesta en marcha

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # y edita SECRET_KEY / ADMIN_PASSWORD
python seed.py                  # crea la BD, el admin y el contenido base
python run.py
```

- Sitio público: http://127.0.0.1:81/  (entra el visitante normal)
- Panel admin: http://127.0.0.1:81/admin  (login en `/login`)

Usuario/contraseña iniciales: los definidos en `.env` (`ADMIN_USERNAME` /
`ADMIN_PASSWORD`), por defecto `admin` / `cambiar123` — **cámbialos**.

> `run.py` escucha en el puerto **81** en modo debug. `config.py` ahora sí
> carga `.env` (antes la variable existía en requirements pero nunca se
> leía, así que el `.env` local no surtía efecto).

### Rutas

| Ruta | Quién entra | Qué hace |
|---|---|---|
| `/` | público | sitio informativo |
| `/admin` | admin | panel: empresa, secciones, acceso |
| `/admin/empresa` | admin | logo, nombre y redes sociales |
| `/admin/contenido/<seccion>` | admin | editar un texto del sitio |
| `/admin/cuenta` | admin | cambiar usuario y contraseña |
| `/login` · `/logout` | — | entrar / salir del panel |
| `/healthz` | — | sonda de vida para Docker (no toca la BD) |

`/admin/cuenta` pide siempre la **contraseña actual** antes de aplicar el
cambio, para que una sesión abierta en un equipo compartido no baste para
cambiarle la contraseña al dueño. La contraseña nueva es opcional: si se
deja vacía, solo cambia el usuario.

### Contacto y accesos en el sitio público

- **Botón flotante de WhatsApp** (`.wa-float`, esquina inferior derecha):
  aparece en cuanto hay un número en *Empresa → WhatsApp* y lleva un
  mensaje precargado, para que el cliente solo tenga que darle *Enviar*.
  En móvil sube para no quedar debajo de la barra inferior. Si no hay
  número configurado, el botón no se renderiza.
- **Acceso al panel** con dos botones discretos, sin candado ni icono: uno
  "Acceso" en la barra de navegación (antes del botón "Contactar", para
  que la llamada a la acción siga siendo lo último) y otro "Acceso
  administrador" en el pie de página. Ambos llevan a `/admin`, que igual
  pide login — esconder la ruta no es seguridad, así que se deja visible
  por comodidad.
- **Hueco del logo siempre reservado**: la cabecera renderiza un `<img>`
  en ambos casos, así el nombre no se mueve al subir el logo real. Sin
  logo configurado muestra `app/static/img/logo-placeholder.svg`, que es
  un SVG provisional de una guayaba con la paleta del sitio. Vive en
  `static/img/` y **no** en `static/uploads/`, para que el volumen de
  Docker no lo tape. Al subir un logo desde el panel, desaparece solo.

## Despliegue en Coolify (Docker Compose)

El proyecto ya incluye `Dockerfile`, `docker-compose.yml` y `entrypoint.sh`.
El contenedor corre **gunicorn** en el puerto **8000** (no el servidor de
desarrollo de Flask) y `entrypoint.sh` ejecuta `seed.py` en cada arranque:
es idempotente, así que solo crea lo que falta y nunca pisa lo que ya
editaste desde el panel.

### 1. Sube el código a un repositorio

Coolify compila desde Git, así que el proyecto debe estar en GitHub/GitLab.
`.gitignore` ya excluye `instance/`, `*.db`, `.env` y `__pycache__/`.

### 2. Crea el recurso en Coolify

- **New Resource → Application → Docker Compose** (o *Public/Private
  Repository* → tipo *Docker Compose*).
- Selecciona el repositorio y la rama.
- Coolify toma el `docker-compose.yml` de la raíz automáticamente.

### 3. Define las variables de entorno (obligatorias)

En **Environment Variables** del recurso:

| Variable | ¿Obligatoria? | Valor |
|---|---|---|
| `SECRET_KEY` | **Sí** | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_PASSWORD` | **Sí** | contraseña fuerte del panel |
| `ADMIN_USERNAME` | No | `admin` por defecto |
| `APP_PORT` | No | puerto en el host; `8000` por defecto |

El compose falla el deploy de forma deliberada si faltan `SECRET_KEY` o
`ADMIN_PASSWORD`, para no publicar el sitio con la clave por defecto.

### 4. Configura el dominio

- **Domains → Add Domain**, apunta a tu dominio (ej. `guayaba-velena.com`).
- Puerto del contenedor: **8000**.
- Coolify enruta por el proxy; no necesitas abrir nada en el firewall.
  La línea `ports` del compose solo sirve para acceso directo por host.

### 5. Despliega

**Deploy**. El primer arranque crea la base, el usuario admin y el
contenido base. Entra al panel y cambia lo que necesites.

### Persistencia y respaldos

Dos volúmenes nombrados sobreviven a redeploys y reinicios:

| Volumen | Ruta en el contenedor | Contenido |
|---|---|---|
| `db_data` | `/app/instance` | `guayaba.db` (SQLite) |
| `uploads` | `/app/app/static/uploads` | logos subidos desde el panel |

> **No uses `docker compose down -v`**: la flag `-v` borra los volúmenes y
> te deja sin sitio. Para respaldar, copia el archivo `guayaba.db` del
> volumen `db_data`.

La foto del hero vive en `app/static/img/guayaba_hero.png`, **fuera** del
volumen de uploads a propósito: si estuviera dentro, el montaje del volumen
la ocultaría y el sitio saldría sin imagen.

### Notas de producción

- Gunicorn corre con **1 worker y 4 hilos**: SQLite no tolera bien varios
  procesos escribiendo a la vez. Para escalar hay dos caminos: subir los
  hilos del compose, o —si el tráfico crece de verdad— migrar a PostgreSQL
  (cambiar `DATABASE_URL` y añadir `psycopg2-binary` a los requirements).
- El contenedor corre como usuario sin privilegios (`app`); ambos
  volúmenes le pertenecen para que pueda escribir.
- La imagen base está fijada a `python:3.13-slim` y las dependencias a
  versiones exactas, así el build es reproducible.

## Notas de diseño

- Un solo registro en `Empresa` (id=1) centraliza logo, nombre y enlaces
  de WhatsApp/Facebook/Instagram/TikTok, consumidos igual por el panel
  público y el admin.
- `Contenido` guarda cada bloque de texto del sitio por clave (`seccion`),
  para editarlo sin tocar plantillas ni código.
- Paleta y tipografía en `static/css/style.css` con estilo agrícola
  (verde guayaba, rosado interior de la fruta, tierra, crema).
