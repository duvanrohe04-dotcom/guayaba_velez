"""
Script de inicialización: crea las tablas, un usuario admin y el contenido
base del sitio a partir de la información entregada por el cliente.

Uso:
    python seed.py
"""
from app import create_app
from app.extensions import db
from app.models import Usuario, Empresa, Contenido

app = create_app()

CONTENIDO_BASE = [
    dict(
        seccion='historia',
        titulo='Nuestra historia',
        texto=(
            'Cultivamos la guayaba regional del municipio de Vélez en la vereda '
            'Guayabal, a una altura aproximada de 1810 msnm. El bocadillo veleño, '
            'elaborado con esta guayaba, cuenta con Denominación de Origen '
            'Protegida y es reconocido en toda Colombia y en Europa.'
        ),
        orden=1,
    ),
    dict(
        seccion='fincas',
        titulo='Nuestras fincas',
        texto=(
            'Los cultivos se desarrollan en la finca Buena Vista y la finca El '
            'Placer, ubicadas en la vereda Guayabal. Los árboles actuales tienen '
            'una edad promedio de 7 años, con una productividad esperada de 40 '
            'años realizando manejos adecuados.'
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

        Empresa.get_instance()  # crea la fila id=1 si no existe

        for datos in CONTENIDO_BASE:
            existente = Contenido.get_por_seccion(datos['seccion'])
            if existente is None:
                db.session.add(Contenido(**datos))
                print(f"Sección creada: {datos['seccion']}")

        db.session.commit()
        print('Seed completado.')


if __name__ == '__main__':
    run_seed()
