"""
Script de inicialización: crea las tablas, un usuario admin y el contenido
base del sitio a partir de la información entregada por el cliente.

Uso:
    python seed.py
"""
from app import create_app
from app.extensions import db
from app.models import Usuario, Empresa, Contenido, Producto

app = create_app()

CONTENIDO_BASE = [
    dict(
        seccion='historia',
        titulo='Nuestra historia',
        texto=(
            'Cultivamos la guayaba regional del municipio de Vélez en la vereda '
            'Guayabal, a una altura aproximada de 1810 msnm, en la zona de '
            'denominación de origen del bocadillo veleño, un dulce reconocido '
            'en toda Colombia y en Europa.'
        ),
        orden=1,
    ),
    dict(
        seccion='fincas',
        titulo='Nuestras fincas',
        texto=(
            'Los cultivos se desarrollan en la finca Buena Vista y la finca El '
            'Placer, ubicadas en la vereda Guayabal, a 7 kilómetros del casco '
            'urbano de Vélez, Santander, vía Vélez–Chipatá. Los árboles actuales '
            'tienen una edad promedio de 7 años, con una productividad esperada '
            'de 40 años realizando manejos adecuados.'
        ),
        orden=2,
    ),
    dict(
        seccion='proceso_productivo',
        titulo='Proceso productivo',
        texto=(
            'Garantizamos una cosecha constante gracias al buen manejo '
            'implementado. A partir del análisis del suelo aportamos los '
            'nutrientes necesarios para la continuidad del ciclo productivo, y '
            'realizamos mejoras del suelo con materias primas orgánicas '
            'disponibles en la región (gallinaza, pollinaza, bagazo de caña de '
            'azúcar y demás). El control de arvenses se hace de manera regular, '
            'principalmente con guadañadora.'
        ),
        orden=3,
    ),
    dict(
        seccion='manejo_fitosanitario',
        titulo='Podas y control de plagas',
        texto=(
            'El proceso de podas se realiza recurrentemente, mediante '
            'diagnósticos constantes y observando el desarrollo del árbol en '
            'sus diversas etapas. El control de plagas y enfermedades se '
            'realiza de manera eficiente y con respaldo profesional, '
            'garantizando las dosis adecuadas y cumpliendo con las Buenas '
            'Prácticas Agrícolas (BPA).'
        ),
        orden=4,
    ),
    dict(
        seccion='cosecha_transformacion',
        titulo='Cosecha y transformación',
        texto=(
            'La recolección se hace de manera regular según la madurez del '
            'fruto, entre una y dos veces por semana, recogiendo frutos sanos y '
            'dando un manejo adecuado a los frutos infestados. El proceso de '
            'transformación se realiza en la planta agroindustrial ubicada en '
            'la vereda Guayabal, lo que minimiza fallas en el transporte y '
            'garantiza una trazabilidad completa hasta el consumidor final: '
            'conserva de guayaba y bocadillo de calidad.'
        ),
        orden=5,
    ),
]


PRODUCTOS_BASE = [
    dict(
        nombre='Conserva natural de guayaba',
        descripcion=('Un producto natural y tradicional, elaborado con guayaba de la '
                     'vereda Guayabal y empacado en calceta de plátano.'),
        etiquetas='🌿 Natural, 🏡 Tradicional, 🍃 Empacada en calceta de plátano',
        cinta='Producto tradicional',
        imagen='img/productos/conserva-hoja.jpg',
        orden=1,
    ),
    dict(
        nombre='Bocadillo rojo',
        descripcion=('El bocadillo rojo de guayaba, dulce y tradicional, hecho con la '
                     'guayaba regional de nuestras fincas.'),
        etiquetas='🍓 Guayaba roja, 🏡 Tradicional, 🤝 Pedidos por encargo',
        cinta='Clásico veleño',
        imagen='img/productos/bocadillo-rojo.jpg',
        orden=2,
    ),
]


def run_seed():
    with app.app_context():
        db.create_all()

        # Solo se crea el admin inicial si la tabla está VACÍA. Antes se buscaba
        # por nombre: si el cliente cambiaba su usuario desde el panel, cada
        # deploy volvía a crear un "admin" nuevo con la contraseña de las
        # variables de entorno (una cuenta de más y con clave conocida).
        if Usuario.query.count() == 0:
            admin = Usuario(username=app.config['ADMIN_USERNAME'])
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            print(f"Usuario admin creado: {app.config['ADMIN_USERNAME']}")
        else:
            print('Ya existen usuarios; no se crea ni se modifica ninguno.')

        empresa = Empresa.get_instance()  # crea la fila id=1 si no existe
        # Corrección de apellido: es "Díaz" (con z), no "Días". Solo toca ese
        # error exacto; cualquier otro nombre que el cliente ponga se respeta.
        if empresa.nombre and 'Días' in empresa.nombre and 'Bocadillos' in empresa.nombre:
            empresa.nombre = empresa.nombre.replace('Días', 'Díaz')
            print(f'Nombre corregido a: {empresa.nombre.strip()}')

        for datos in CONTENIDO_BASE:
            existente = Contenido.get_por_seccion(datos['seccion'])
            if existente is None:
                db.session.add(Contenido(**datos))
                print(f"Sección creada: {datos['seccion']}")

        # Corrección de "Nuestra historia": ya no dice que "cuenta con Denominación de
        # Origen Protegida", sino que está en la zona de denominación de origen. Solo
        # se reemplaza si el texto sigue siendo el original del seed (si el
        # administrador lo editó, no se toca).
        historia = Contenido.get_por_seccion('historia')
        historia_vieja = (
            'Cultivamos la guayaba regional del municipio de Vélez en la vereda '
            'Guayabal, a una altura aproximada de 1810 msnm. El bocadillo veleño, '
            'elaborado con esta guayaba, cuenta con Denominación de Origen '
            'Protegida y es reconocido en toda Colombia y en Europa.'
        )
        if historia is not None and historia.texto == historia_vieja:
            historia.texto = [d for d in CONTENIDO_BASE if d['seccion'] == 'historia'][0]['texto']
            print('Texto de "Nuestra historia" corregido (zona de denominación de origen).')

        # "Nuestras fincas": se añade la ubicación (7 km del casco urbano, vía
        # Vélez–Chipatá). Solo si el texto sigue siendo el original del seed.
        fincas = Contenido.get_por_seccion('fincas')
        fincas_vieja = (
            'Los cultivos se desarrollan en la finca Buena Vista y la finca El '
            'Placer, ubicadas en la vereda Guayabal. Los árboles actuales tienen '
            'una edad promedio de 7 años, con una productividad esperada de 40 '
            'años realizando manejos adecuados.'
        )
        if fincas is not None and fincas.texto == fincas_vieja:
            fincas.texto = [d for d in CONTENIDO_BASE if d['seccion'] == 'fincas'][0]['texto']
            print('Texto de "Nuestras fincas" actualizado con la ubicación.')

        # Corrección de redacción: "hoja de plátano" -> "calceta de plátano" en el
        # producto inicial ya guardado. Solo se cambia si el texto sigue siendo el
        # original; si el administrador lo editó, no se toca.
        for prod in Producto.query.filter_by(nombre='Conserva natural de guayaba').all():
            if prod.descripcion == ('Un producto natural y tradicional, elaborado con guayaba de la '
                                    'vereda Guayabal y empacado en hoja de plátano.'):
                prod.descripcion = prod.descripcion.replace('hoja de plátano', 'calceta de plátano')
                print('Descripción del producto corregida (calceta de plátano).')
            if prod.etiquetas == '🌿 Natural, 🏡 Tradicional, 🍃 Empacada en hoja de plátano':
                prod.etiquetas = prod.etiquetas.replace('hoja de plátano', 'calceta de plátano')
                print('Etiqueta del producto corregida (calceta de plátano).')

        # Productos iniciales: se crean UNA sola vez. La marca '_productos_semilla'
        # evita que, si el administrador los borra o los cambia, un deploy los
        # vuelva a crear.
        if Contenido.get_por_seccion('_productos_semilla') is None:
            if Producto.query.count() == 0:
                for datos in PRODUCTOS_BASE:
                    db.session.add(Producto(**datos))
                print('Productos iniciales creados.')
            db.session.add(Contenido(seccion='_productos_semilla', titulo='marca interna', texto='1', orden=999))

        db.session.commit()
        print('Seed completado.')


if __name__ == '__main__':
    run_seed()
