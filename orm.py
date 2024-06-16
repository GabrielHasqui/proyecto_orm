from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Avg, F,Q, OuterRef, Subquery, Count, Max, Min, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import timedelta
from django.db.models.functions import Length

from core.models import Periodo, Asignatura, Profesor, Estudiante, Nota, DetalleNota

def insertar_datos_orm():
    def create_user():
        user, created = User.objects.get_or_create(username='poo', email='dan@example.com')
        if created:
            user.set_password('1234')
            user.save()
            print("Nuevo usuario creado:", user)
        else:
            print("Usuario existente encontrado:", user)
        return user

    def insertar_periodos(user):
        periodos_data = [
            '2024-2025', '2023-2024', '2022-2023', '2021-2022', '2020-2021',
            '2019-2020', '2018-2019', '2017-2018', '2016-2017', '2015-2016'
        ]
        periodos = [Periodo(user=user, periodo=p) for p in periodos_data]
        periodos_creados = Periodo.objects.bulk_create(periodos, ignore_conflicts=True)
        print(f'Se han creado {len(periodos_creados)} periodos académicos.')

    def insertar_asignaturas(user):
        asignaturas_data = [
            'Matemáticas10', 'Física', 'Programación', 'Literatura', 'Historia',
            'Biología', 'Química', 'Geografía', 'Arte', 'Música'
        ]
        asignaturas = [Asignatura(user=user, descripcion=a) for a in asignaturas_data]
        asignaturas_creadas = Asignatura.objects.bulk_create(asignaturas, ignore_conflicts=True)
        print(f'Se han creado {len(asignaturas_creadas)} asignaturas.')

    def insertar_profesores(user):
        profesores_data = [
            ('Juan Pérez', '1234567890'), ('María González', '0987654321'), 
            ('Luis Ramírez', '5432167890'), ('Ana Martínez', '0987654321'), 
            ('Carlos Sánchez', '1234509876'), ('Laura Gómez', '6789054321'), 
            ('Pedro Castro', '5432109876'), ('Lucía Herrera', '0987654321'), 
            ('Miguel Ruiz', '1234567890'), ('Sofía López', '5678901234')
        ]
        profesores = [Profesor(user=user, nombre=p[0], dni=p[1]) for p in profesores_data]
        profesores_creados = Profesor.objects.bulk_create(profesores, ignore_conflicts=True)
        print(f'Se han creado {len(profesores_creados)} profesores.')

    def insertar_estudiantes(user):
        estudiantes_data = [
            ('Estudiante 1', '1111111111'), ('Estudiante 2', '2222222222'), 
            ('Estudiante 3', '3333333333'), ('Estudiante 4', '4444444444'), 
            ('Estudiante 5', '5555555555'), ('Estudiante 6', '6666666666'), 
            ('Estudiante 7', '7777777777'), ('Estudiante 8', '8888888888'), 
            ('Estudiante 9', '9999999999'), ('Estudiante 10', '1010101010')
        ]
        estudiantes = [Estudiante(user=user, nombre=e[0], dni=e[1]) for e in estudiantes_data]
        estudiantes_creados = Estudiante.objects.bulk_create(estudiantes, ignore_conflicts=True)
        print(f'Se han creado {len(estudiantes_creados)} estudiantes.')

    def insertar_notas(user):
        periodos = list(Periodo.active_objects.filter(state=True))
        asignaturas = list(Asignatura.active_objects.filter(state=True))
        profesores = list(Profesor.active_objects.filter(state=True))

        notas = [
            Nota(user=user, periodo=periodos[i % len(periodos)], profesor=profesores[i % len(profesores)], asignatura=asignaturas[i % len(asignaturas)])
            for i in range(10)
        ]
        notas_creadas = Nota.objects.bulk_create(notas, ignore_conflicts=True)
        print(f'Se han creado {len(notas_creadas)} notas.')

    def insertar_detalle_notas(user):
        notas = list(Nota.active_objects.filter(state=True))
        estudiantes = list(Estudiante.active_objects.filter(state=True))

        registros_predefinidos = [
            {'nota1': 6.5, 'nota2': 6.0, 'recuperacion': 8.0, 'observacion': 'Bueno', 'fecha_creacion': datetime(2022, 12, 31)},
            {'nota1': 6.0, 'nota2': 9.5, 'recuperacion': None, 'observacion': 'Excelente', 'fecha_creacion': datetime(2022, 12, 30)},
            {'nota1': 8.5, 'nota2': 7.5, 'recuperacion': 7.0, 'observacion': 'Aprobado', 'fecha_creacion': datetime(2022, 12, 29)},
            {'nota1': 7.0, 'nota2': 6.5, 'recuperacion': 8.0, 'observacion': 'Reprobado', 'fecha_creacion': datetime(2024, 3, 28)},
            {'nota1': 6.5, 'nota2': 9.0, 'recuperacion': None, 'observacion': 'Bueno', 'fecha_creacion': datetime(2022, 3, 27)},
            {'nota1': 9.0, 'nota2': 7.0, 'recuperacion': 8.5, 'observacion': 'Excelente', 'fecha_creacion': datetime(2022, 12, 26)},
            {'nota1': 8.0, 'nota2': 6.0, 'recuperacion': 7.5, 'observacion': 'Necesita mejorar', 'fecha_creacion': datetime(2023, 1, 2)},
            {'nota1': 5.5, 'nota2': 8.0, 'recuperacion': 9.0, 'observacion': 'Bueno', 'fecha_creacion': datetime(2023, 3, 3)},
            {'nota1': 7.8, 'nota2': 7.2, 'recuperacion': None, 'observacion': 'Aprobado', 'fecha_creacion': datetime(2023, 1, 4)},
            {'nota1': 6.9, 'nota2': 8.1, 'recuperacion': 7.9, 'observacion': 'Excelente', 'fecha_creacion': datetime(2023, 1, 5)},
        ]

        detalle_notas = []

        for i, record in enumerate(registros_predefinidos):
            nota = notas[i % len(notas)]
            estudiante = estudiantes[i % len(estudiantes)]

            if not DetalleNota.objects.filter(nota=nota, estudiante=estudiante).exists():
                detalle_nota = DetalleNota(
                    user=user,
                    nota=nota,
                    estudiante=estudiante,
                    nota1=record['nota1'],
                    nota2=record['nota2'],
                    recuperacion=record['recuperacion'],
                    observacion=record['observacion'],
                    created=record['fecha_creacion']
                )
                detalle_notas.append(detalle_nota)

        detalle_notas_creadas = DetalleNota.objects.bulk_create(detalle_notas, ignore_conflicts=True)
        print(f'Se han creado {len(detalle_notas_creadas)} detalles de notas.')

    user = create_user()
    insertar_periodos(user)
    insertar_asignaturas(user)
    insertar_profesores(user)
    insertar_estudiantes(user)
    insertar_notas(user)
    insertar_detalle_notas(user)

# Consultas Básicas:

# 1. Seleccionar todos los estudiantes cuyo nombre comienza con 'Est':
def get_estudiantes_by_nombre_prefix(prefix):
    return Estudiante.active_objects.filter(nombre__startswith=prefix, state=True)
def buscar_y_mostrar_estudiantes(prefix):
    estudiantes = get_estudiantes_by_nombre_prefix(prefix)
    for estudiante in estudiantes:
        print(estudiante.nombre)

# 2. Seleccionar todos los profesores cuyo nombre contiene 'or':
def get_profesores_by_nombre_contains(substring):
    return Profesor.active_objects.filter(nombre__icontains=substring, state=True)
def buscar_y_mostrar_profesores(substring):
    profesores = get_profesores_by_nombre_contains(substring)
    for profesor in profesores:
        print(profesor.nombre)

# 3. Seleccionar todas las asignaturas cuya descripción termina en '10':
def get_asignaturas_by_descripcion_suffix(suffix):
    return Asignatura.active_objects.filter(descripcion__endswith=suffix, state=True)
def buscar_y_mostrar_asignaturas(suffix):
    asignaturas = get_asignaturas_by_descripcion_suffix(suffix)
    for asignatura in asignaturas:
        print(asignatura.descripcion)

# 4. Seleccionar todas las notas con nota1 mayor que 8.0:
def get_notas_by_nota1_gt(threshold):
    return DetalleNota.active_objects.filter(nota1__gt=threshold, state=True)
def buscar_y_mostrar_notas_por_nota1(threshold):
    notas = get_notas_by_nota1_gt(threshold)
    for nota in notas:
        print(f'Nota1: {nota.nota1}')

# 5. Seleccionar todas las notas con nota2 menor que 9.0:
def get_notas_by_nota2_lt(threshold):
    return DetalleNota.active_objects.filter(nota2__lt=threshold, state=True)
def buscar_y_mostrar_notas_por_nota2(threshold):
    notas = get_notas_by_nota2_lt(threshold)
    for nota in notas:
        print(f'Nota2: {nota.nota2}')
# 6. Seleccionar todas las notas con recuperación igual a 9.5:
def get_notas_by_recuperacion_equals(value):
    return DetalleNota.active_objects.filter(recuperacion=value, state=True)
def buscar_y_mostrar_notas_por_recuperacion(value):
    notas = get_notas_by_recuperacion_equals(value)
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Recuperación: {nota.recuperacion}')

            
#   Consultas usando condiciones lógicas (AND, OR, NOT)
def get_estudiantes_by_nombre_prefix_and_dni_suffix(prefix, suffix):
    return Estudiante.active_objects.filter(state=True, nombre__startswith=prefix) & Estudiante.active_objects.filter(dni__endswith=suffix)

def buscar_y_mostrar_estudiantes_por_prefix_y_suffix(prefix, suffix):
    estudiantes = get_estudiantes_by_nombre_prefix_and_dni_suffix(prefix, suffix)
    for estudiante in estudiantes:
        print(estudiante.nombre)

def get_asignaturas_by_descripcion_contains_or_suffix(contains, suffix):
    return Asignatura.active_objects.filter(state=True).filter(Q(descripcion__contains=contains) | Q(descripcion__endswith=suffix))

def buscar_y_mostrar_asignaturas_por_contains_o_suffix(contains, suffix):
    asignaturas = get_asignaturas_by_descripcion_contains_or_suffix(contains, suffix)
    for asignatura in asignaturas:
        print(asignatura.descripcion)

def get_profesores_by_nombre_not_contains(substring):
    return Profesor.active_objects.filter(state=True).exclude(nombre__icontains=substring)

def buscar_y_mostrar_profesores_por_nombre_no_contains(substring):
    profesores = get_profesores_by_nombre_not_contains(substring)
    for profesor in profesores:
        print(profesor.nombre)

def get_notas_by_nota1_gt_and_nota2_lt(nota1_threshold, nota2_threshold):
    return DetalleNota.active_objects.filter(state=True, nota1__gt=nota1_threshold) & DetalleNota.active_objects.filter(nota2__lt=nota2_threshold)

def buscar_y_mostrar_notas_por_nota1_y_nota2(nota1_threshold, nota2_threshold):
    notas = get_notas_by_nota1_gt_and_nota2_lt(nota1_threshold, nota2_threshold)
    for nota in notas:
        print(f'Nota1: {nota.nota1}, Nota2: {nota.nota2}')

def get_notas_by_recuperacion_is_null_or_nota2_gt(value):
    return DetalleNota.active_objects.filter(state=True).filter(Q(recuperacion__isnull=True) | Q(nota2__gt=value))

def buscar_y_mostrar_notas_por_recuperacion_is_null_o_nota2(value):
    notas = get_notas_by_recuperacion_is_null_or_nota2_gt(value)
    for nota in notas:
        print(f'Recuperacion: {nota.recuperacion}, Nota2: {nota.nota2}')       
            
#Consultas usando funciones númericas
def seleccionar_notas_nota1_7a9():
    notas = DetalleNota.active_objects.filter(nota1__gte=7.0, nota1__lte=9.0)
        
    print("Notas de estudiantes con nota 1 entre 7.00 y 9.00 puntos")
    if notas:
        for nota in notas:
            print(f'- Nota#{nota.id} - Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}, Observación: {nota.observacion}')
    else:
        print("No hay notas registradas con esas caracteristicas")

def seleccionar_notas_fuerade_6y8():
    notas_fuera_rango = DetalleNota.active_objects.exclude(nota2__gte=6.0, nota2__lte=8.0)

    if notas_fuera_rango:
        print("Notas de estudiantes con nota2 fuera de el rango de 6 a 8 puntos")
        for nota in notas_fuera_rango:
            print(f'- Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}, Observación: {nota.observacion}')
    else:
        print("No hay notas registradas con esas caracteristicas")

#poner blank_True y null=True en Tabla DetallesNota, en campo recuperacion
def seleccionar_recuperacion_notNone():
    notas_con_recuperacion = DetalleNota.active_objects.exclude(recuperacion__isnull=True)
    print("Notas de estudiantes con recuperacion diferente de None: ")
    if notas_con_recuperacion:
        for nota in notas_con_recuperacion:
            print(f'- Nota#{nota.id} Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}, Observación: {nota.observacion}')
    else:
        print("No hay notas registradas con esas caracteristicas")
       
            
# Consultas usando funciones de fecha:

# 15. Seleccionar todas las notas creadas en el último año:
def notas_ultimo_anio():
    fecha_actual = timezone.now()
    fecha_inicio = fecha_actual - timedelta(days=365)
    return DetalleNota.active_objects.filter(created__gte=fecha_inicio, state=True)
def buscar_y_mostrar_notas_ultimo_anio():
    notas = notas_ultimo_anio()
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 16. Seleccionar todas las notas creadas en el último mes:
def notas_ultimo_mes():
    fecha_actual = timezone.now()
    fecha_inicio = fecha_actual - timedelta(days=30)
    return DetalleNota.active_objects.filter(created__gte=fecha_inicio, state=True)

def buscar_y_mostrar_notas_ultimo_mes():
    notas = notas_ultimo_mes()
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 17. Seleccionar todas las notas creadas en el último día:
def notas_ultimo_dia():
    fecha_actual = timezone.now()
    fecha_inicio = fecha_actual - timedelta(days=1)
    return DetalleNota.active_objects.filter(created__gte=fecha_inicio, state=True)

def buscar_y_mostrar_notas_ultimo_dia():
    notas = notas_ultimo_dia()
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 18. Seleccionar todas las notas creadas antes del año 2023:
def notas_antes_2023():
    return DetalleNota.active_objects.filter(created__lt=datetime(2023, 1, 1), state=True)

def buscar_y_mostrar_notas_antes_2023():
    notas = notas_antes_2023()
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 19. Seleccionar todas las notas creadas en marzo de cualquier año:
def notas_marzo_cualquier_anio():
    return DetalleNota.active_objects.filter(created__month=3, state=True)

def buscar_y_mostrar_notas_marzo_cualquier_anio():
    notas = notas_marzo_cualquier_anio()
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')
            
# Consultas combinadas con funciones avanzadas

def get_estudiantes_nombre_exact_length(length):
    return Estudiante.active_objects.filter(state=True).annotate(nombre_length=Length('nombre')).filter(nombre_length=length)

def buscar_y_mostrar_estudiantes_por_nombre_length(length):
    estudiantes = get_estudiantes_nombre_exact_length(length)
    for estudiante in estudiantes:
        print(estudiante.nombre)

def get_notas_by_nota1_and_nota2_gt(value):
    return DetalleNota.active_objects.filter(state=True, nota1__gt=value, nota2__gt=value)

def buscar_y_mostrar_notas_por_nota1_y_nota2_gt(value):
    notas = get_notas_by_nota1_and_nota2_gt(value)
    for nota in notas:
        print(f'Nota1: {nota.nota1}, Nota2: {nota.nota2}')

def get_notas_by_recuperacion_not_null_and_nota1_gt_nota2():
    return DetalleNota.active_objects.filter(state=True, recuperacion__isnull=False).filter(nota1__gt=F('nota2'))

def buscar_y_mostrar_notas_por_recuperacion_y_nota1_gt_nota2():
    notas = get_notas_by_recuperacion_not_null_and_nota1_gt_nota2()
    for nota in notas:
        print(f'Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperacion: {nota.recuperacion}')

def get_notas_by_nota1_gt_or_nota2_equals(value1, value2):
    return DetalleNota.active_objects.filter(state=True).filter(Q(nota1__gt=value1) | Q(nota2=value2))

def buscar_y_mostrar_notas_por_nota1_o_nota2(value1, value2):
    notas = get_notas_by_nota1_gt_or_nota2_equals(value1, value2)
    for nota in notas:
        print(f'Nota1: {nota.nota1}, Nota2: {nota.nota2}')

def get_notas_by_recuperacion_gt_nota1_and_nota2():
    return DetalleNota.active_objects.filter(state=True).filter(Q(recuperacion__gt=F('nota1')) & Q(recuperacion__gt=F('nota2')))

def buscar_y_mostrar_notas_por_recuperacion_gt_nota1_y_nota2():
    notas = get_notas_by_recuperacion_gt_nota1_and_nota2()
    for nota in notas:
        print(f'Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperacion: {nota.recuperacion}')


#Consultas con subconsultos y anotaciones
def seleccionar_estudiantes_nota_recuperacion():

    subquery = DetalleNota.active_objects.filter(
        estudiante=OuterRef('pk'),
        recuperacion__isnull=False
    ).values('id')[:1]

    estudiantes_con_recuperacion = Estudiante.objects.filter(
        id__in=Subquery(subquery.values('estudiante'))
    )

    print("Estudiantes con al menos una nota de recuperación: ")
    if estudiantes_con_recuperacion:
        for estudiante in estudiantes_con_recuperacion:
            print(f'Estudiante: {estudiante.nombre} - id: #{estudiante.id}')
    else:
        print("No hay ningun estudiante con nota de recuperacion")

def profesores_con_asignatura_especifica():
    asignatura_id = 9
    asignatura = Asignatura.objects.get(pk=asignatura_id)

    subquery = Nota.active_objects.filter(
        asignatura__id=asignatura_id,
        profesor_id=OuterRef('pk')
    ).values('id')[:1]

    profesores = Profesor.objects.filter(
        id__in=Subquery(subquery.values('profesor_id'))
    ).distinct()

    print(f"Profesores que han dado la asignatura {asignatura.descripcion}")
    if profesores:
        for profesor in profesores:
            print(f"- Id: #{profesor.id} - Profesor: {profesor.nombre}")
    else:
        print(f"Ningun profesor ha dado la asignatura {asignatura.descripcion}")

def asignatura_con_nota():
    asignaturas_con_notas = Asignatura.active_objects.annotate(num_notas=Count('nota')).filter(num_notas__gt=0)

    print("Asignaturas con notas registradas: ")
    if asignaturas_con_notas:
        for asignatura in asignaturas_con_notas:
            print(f"Id: #{asignatura.id} - {asignatura.descripcion}")
    else:
        print("No hay asignaturas con notas registradas")

def asignatura_sin_notas():
    asignaturas_sin_notas = Asignatura.active_objects.annotate(num_notas=Count('nota')).filter(num_notas=0)

    print("Asignaturas sin notas registradas: ")
    if asignatura_sin_notas:
        for asignatura in asignaturas_sin_notas:
            print(asignatura.descripcion)
    else:
        print("Todas las asignaturas estan en una nota")

def seleccionar_estudiantes_sin_nota_recuperacion():
    estudiantes_con_recuperacion = DetalleNota.active_objects.filter(
        recuperacion__isnull=False
    ).values('estudiante_id').distinct()

    estudiantes_sin_recuperacion = Estudiante.active_objects.exclude(
        id__in=Subquery(estudiantes_con_recuperacion)
    )
    print("Estudiantes sin notas de recuperación: ")
    if estudiantes_sin_recuperacion:
        for estudiante in estudiantes_sin_recuperacion:
            print(f"- Id: #{estudiante.id} - {estudiante.nombre}")
    else:
        print("Todos los estudiantes poseen una nota de recuperacion")
        
def notas_promedio_mayor_8():
    detalles_con_suma_mayor_a_8 = DetalleNota.active_objects.annotate(
        promedio=(F('nota1') + F('nota2')) / 2
    ).filter(promedio__gt=8.0)
        
    print("Notas con promedio de nota1 y nota2 que es mayor a 8 puntos:")
    if detalles_con_suma_mayor_a_8:
        for detalle in detalles_con_suma_mayor_a_8:
            promedio = (detalle.nota1 + detalle.nota2) / 2
            promedio = "{:.2f}".format(promedio)
            print(F"- Nota ID: {detalle.id} - Estudiante: {detalle.estudiante.nombre} - Promedio: {promedio} - Asignatura: {detalle.nota.asignatura.descripcion}")
    else:
        print("No hay ninguna nota con promedio mayor a 8 puntos")

def notas_nota1_menora6_nota2_mayora7():
    notas_filtradas = DetalleNota.active_objects.annotate(
        condicion=Q(nota1__lt=6.0) & Q(nota2__gt=7.0)
    ).filter(condicion=True)

    print("Notas de estudiantes con nota1 menor a 6 y nota2 mayor a 7")
    if notas_filtradas:
        for nota in notas_filtradas:
            print(f"- Nota ID: {nota.nota.id} - Nota1: {nota.nota1} - Nota2: {nota.nota2} - Estudiante: {nota.estudiante.nombre}")
    else:
        print("No hay notas registradas que cumplan la condicion")

def notas_nota1_en_lista():
    lista_notas = [7.0, 8.0, 9.0]

    detalles_filtrados = DetalleNota.active_objects.filter(nota1__in=lista_notas)

    print("Notas de estudiantes con nota 1 en la lista [7.0, 8.0, 9.0]")
    if detalles_filtrados:
        for detalle in detalles_filtrados:
            print(f"- Nota ID: {detalle.nota.id} - Nota1: {detalle.nota1} - Estudiante: {detalle.estudiante.nombre}")
    else:
        print("No hay ninguna nota que su nota1 esté en la lista")

def notas_en_rango_id1a5():
    rango_ids = range(1, 6)

    notas_en_rango = DetalleNota.active_objects.filter(id__in=rango_ids)

    print("Notas que su id está en el rango de 1 a 6: ")
    if notas_en_rango:
        for nota in notas_en_rango:
            print(f"Nota ID: {nota.nota.id} - Estudiante: {nota.estudiante.nombre} - nota1: {nota.nota1} - nota2: {nota.nota2} - recuperacion: {nota.recuperacion} - obervacion: {nota.observacion}")
    else:
        print("No hay notas con el id en ese rango")

def notas_recuperacion_noLista():
    recuperaciones_excluir = [8.0, 9.0, 10.0]

    notas_sin_recuperacion = DetalleNota.active_objects.exclude(
        Q(recuperacion__in=recuperaciones_excluir) | Q(recuperacion__isnull=True)
    )

    print("Notas de estudiantes que su recuperacion no están en la lista [8.0, 9.0, 10.0]: ")
    if notas_sin_recuperacion:
        for nota in notas_sin_recuperacion:
            print(f"- Nota ID: {nota.id} - Estudiante: {nota.estudiante} - Recuperacion: {nota.recuperacion}")
    else:
        print("No hay notas que su recuperacion no esté en la lista")

def suma_notas_de_estudiante():
    id_estudiante = 4
    try:
        estudiante = Estudiante.active_objects.get(pk=id_estudiante)
        suma_notas = DetalleNota.active_objects.filter(estudiante_id=id_estudiante).aggregate(
            suma_total = Sum('nota1') + Sum('nota2') +  Sum('recuperacion')
        )

        print(f"Suma total de notas de {estudiante.nombre}")
        if suma_notas['suma_total']:
            print(f"La suma total de notas del estudiante {estudiante.nombre} es: ", suma_notas['suma_total'])
        else:
            print("No hay notas registradas del estudiante")
    except ObjectDoesNotExist:
        print("El estudiante no existe")

def nota_maxima_estudiante():
    id_estudiante = 4
    try:
        estudiante = Estudiante.active_objects.get(pk=id_estudiante)

        notas_estudiante = DetalleNota.active_objects.filter(estudiante_id=id_estudiante)
        nota_maxima = notas_estudiante.aggregate(max_nota=Max(F('nota1') + F('nota2')))['max_nota']
        print("Nota maxima de un estudiante: ")

        if nota_maxima:
            print(f'Nota maxima de {estudiante.nombre}: {nota_maxima}')
        else:
            print(f"{estudiante.nombre} no tiene notas registradas")
    except ObjectDoesNotExist:
        print("El estudiante no existe")

def nota_minima_estudiante():
    id_estudiante = 4
    try:
        estudiante = Estudiante.active_objects.get(pk=id_estudiante)

        notas_estudiante = DetalleNota.active_objects.filter(estudiante_id=id_estudiante)
        nota_minima = notas_estudiante.aggregate(min_nota=Min(F('nota1') + F('nota2')))['min_nota']
        print("Nota minima registrada de un estudiante: ")
        if nota_minima:
            print(f'Nota minima de {estudiante.nombre}: {nota_minima}')
        else:
            print(f"{estudiante.nombre} no tiene notas registradas")
    except ObjectDoesNotExist:
          print("El estudiante no existe")

def notas_total_estudiante():
    id_estudiante = 4
    try:
        estudiante = Estudiante.active_objects.get(pk=id_estudiante)
        num_notas = DetalleNota.active_objects.filter(estudiante_id=id_estudiante).count()
        print("Numero de notas registradas de un estudiante: ")
        if num_notas > 0:
            print(F"El estudiante {estudiante.nombre} tiene {num_notas} notas registradas")
        else:
            print(f"{estudiante.nombre} no tiene ninguna nota registrada")
    except ObjectDoesNotExist:
        print("El estudiante no existe")

def promedio_notas_estudiante():
    id_estudiante = 4
    try:
        estudiante = Estudiante.active_objects.get(pk=id_estudiante)

        notas_estudiante = DetalleNota.active_objects.filter(estudiante_id=id_estudiante)

        suma_notas = 0
        contador_notas_validas = 0

        for nota in notas_estudiante:
            suma_notas += nota.nota1 + nota.nota2
            contador_notas_validas += 1
        print("Promedio de notas de un estudiante: ")
        if contador_notas_validas > 0:
            promedio = suma_notas / (2 * contador_notas_validas)
            print(f"El promedio de notas del estudiante {estudiante.nombre} es: {promedio:.2f}")
        else:
            print(f"No se encontraron notas válidas para el estudiante {estudiante.nombre}")
    except ObjectDoesNotExist:
        print("El estudiante no existe")
        
# Consultas con subconsultas y relaciones inversas:

# 40. Dado un estudiante, obtener todas sus notas con el detalle de todos sus datos relacionados:
def notas_por_estudiante(estudiante_id):
    return DetalleNota.active_objects.filter(estudiante_id=estudiante_id, state=True).select_related('nota', 'nota__periodo', 'nota__profesor', 'nota__asignatura')

def buscar_y_mostrar_notas_por_estudiante(estudiante_id):
    notas = notas_por_estudiante(estudiante_id)
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 41. Obtener todas las notas de un período específico:
def notas_por_periodo(periodo_id):
    return Nota.active_objects.filter(periodo_id=periodo_id, state=True)

def buscar_y_mostrar_notas_por_periodo(periodo_id):
    notas = notas_por_periodo(periodo_id)
    for nota in notas:
        print(f'Nota ID: {nota.id}, Profesor: {nota.profesor.nombre}, Asignatura: {nota.asignatura.descripcion}')

# 42. Consultar todas las notas de una asignatura dada en un período:
def notas_por_asignatura_y_periodo(asignatura_id, periodo_id):
    return Nota.active_objects.filter(asignatura_id=asignatura_id, periodo_id=periodo_id, state=True)

def buscar_y_mostrar_notas_por_asignatura_y_periodo(asignatura_id, periodo_id):
    notas = notas_por_asignatura_y_periodo(asignatura_id, periodo_id)
    for nota in notas:
        print(f'Nota ID: {nota.id}, Profesor: {nota.profesor.nombre}, Asignatura: {nota.asignatura.descripcion}')

# 43. Obtener todas las notas de un profesor en particular:
def notas_por_profesor(profesor_id):
    return Nota.active_objects.filter(profesor_id=profesor_id, state=True)

def buscar_y_mostrar_notas_por_profesor(profesor_id):
    notas = notas_por_profesor(profesor_id)
    for nota in notas:
        print(f'Nota ID: {nota.id}, Profesor: {nota.profesor.nombre}, Asignatura: {nota.asignatura.descripcion}')

# 44. Consultar todas las notas de un estudiante con notas superiores a un valor dado:
def notas_estudiante_con_valor_mayor(estudiante_id, valor):
    return DetalleNota.active_objects.filter(estudiante_id=estudiante_id, nota1__gt=valor, state=True)

def buscar_y_mostrar_notas_estudiante_con_valor_mayor(estudiante_id, valor):
    notas = notas_estudiante_con_valor_mayor(estudiante_id, valor)
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 45. Obtener todas las notas de un estudiante ordenadas por período:
def notas_estudiante_ordenadas_por_periodo(estudiante_id):
    return DetalleNota.active_objects.filter(estudiante_id=estudiante_id, state=True).order_by('nota__periodo__fecha_inicio')

def buscar_y_mostrar_notas_estudiante_ordenadas_por_periodo(estudiante_id):
    notas = notas_estudiante_ordenadas_por_periodo(estudiante_id)
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Período: {nota.nota.periodo.periodo}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 46. Consultar la cantidad total de notas para un estudiante:
def total_notas_estudiante(estudiante_id):
    return DetalleNota.active_objects.filter(estudiante_id=estudiante_id, state=True).count()

def mostrar_total_notas_estudiante(estudiante_id):
    total = total_notas_estudiante(estudiante_id)
    print(f'El total de notas para el estudiante {estudiante_id} es {total}')

# 47. Calcular el promedio de las notas de un estudiante en un período dado:
def promedio_notas_estudiante_periodo(estudiante_id, periodo_id):
    return DetalleNota.active_objects.filter(estudiante_id=estudiante_id, nota__periodo_id=periodo_id, state=True).aggregate(promedio=Avg('nota1'))['promedio']

def mostrar_promedio_notas_estudiante_periodo(estudiante_id, periodo_id):
    promedio = promedio_notas_estudiante_periodo(estudiante_id, periodo_id)
    print(f'El promedio de las notas del estudiante {estudiante_id} en el período {periodo_id} es {promedio}')

# 48. Consultar todas las notas con una observación específica:
def notas_con_observacion(observacion):
    return DetalleNota.active_objects.filter(observacion__icontains=observacion, state=True)

def buscar_y_mostrar_notas_con_observacion(observacion):
    notas = notas_con_observacion(observacion)
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Observación: {nota.observacion}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# 49. Obtener todas las notas de un estudiante ordenadas por asignatura:
def notas_estudiante_ordenadas_por_asignatura(estudiante_id):
    return DetalleNota.active_objects.filter(estudiante_id=estudiante_id, state=True).order_by('nota__asignatura__descripcion')

def buscar_y_mostrar_notas_estudiante_ordenadas_por_asignatura(estudiante_id):
    notas = notas_estudiante_ordenadas_por_asignatura(estudiante_id)
    for nota in notas:
        print(f'Estudiante: {nota.estudiante.nombre}, Asignatura: {nota.nota.asignatura.descripcion}, Nota1: {nota.nota1}, Nota2: {nota.nota2}, Recuperación: {nota.recuperacion}')

# Sentencias Update

def actualizar_nota1_para_menores(threshold):
    DetalleNota.active_objects.filter(state=True, nota1__lt=threshold).update(nota1=20)
    print(f'Se han actualizado las notas1 para estudiantes con nota1 < {threshold}.')

def actualizar_nota2_para_menores(threshold):
    DetalleNota.active_objects.filter(state=True, nota2__lt=threshold).update(nota2=15)
    print(f'Se han actualizado las notas2 para estudiantes con nota2 < {threshold}.')

def actualizar_recuperacion_para_menores(threshold):
    DetalleNota.active_objects.filter(state=True, recuperacion__lt=threshold).update(recuperacion=10)
    print(f'Se han actualizado las recuperaciones para estudiantes con recuperación < {threshold}.')

def actualizar_observacion_para_aprobados():
    DetalleNota.active_objects.filter(state=True, nota1__gte=5.0, nota2__gte=5.0).update(observacion='Aprobado')
    print('Se han actualizado las observaciones para estudiantes aprobados.')

def actualizar_notas_en_periodo(periodo):
    DetalleNota.active_objects.filter(state=True, nota__periodo=periodo).update(nota1=10, nota2=10, recuperacion=10, observacion='Actualizado')
    print(f'Se han actualizado todas las notas en el período {periodo}.')


#sentencias delete
def eliminar_notas_estudiante_fisica():
    id_estudiante = 8
    print("Eliminar fisicamente todas las notas de un estudiante: ")
    try:
        estudiante = Estudiante.active_objects.get(pk=id_estudiante)

        notas_estudiante = DetalleNota.objects.filter(estudiante_id=id_estudiante)
        cantidad_eliminada, _ = notas_estudiante.delete()
        if cantidad_eliminada > 0:
            print(f"Se han eliminado {cantidad_eliminada} notas del estudiante {estudiante.nombre}")
        else:
            print(f"{estudiante.nombre} no tiene notas registradas")
    except ObjectDoesNotExist:
        print("No existe el estudiante")

def eliminar_logicamente_notas_estudiantes():
    id_estudiante = 4
    print("Eliminar logicamente las notas de un estudiante: ")
    try:
        estudiante = Estudiante.active_objects.get(pk=id_estudiante)

        notas_estudiante = DetalleNota.active_objects.filter(estudiante_id=id_estudiante)
        if notas_estudiante:
            for nota in notas_estudiante:
                nota.delete()

            print(f"Se han eliminado lógicamente las notas del estudiante {estudiante.nombre}")
        else:
            print(f"{estudiante.nombre} no tiene notas registradas")
    except ObjectDoesNotExist:
        print("No existe el estudiante")

def eliminar_fisicamente_notas_de_periodo():
    periodo_id = 3
    print("Eliminar fisicamente todas las notas de un periodo")
    try: 
        periodo = Periodo.active_objects.get(pk=periodo_id)
        notas_a_eliminar = Nota.objects.filter(periodo_id=periodo_id)
        if notas_a_eliminar:
            notas_a_eliminar.delete()
            print(f"Se han eliminado todas las notas del período {periodo.periodo}.")
        else:
            print(f"No hay notas en el periodo {periodo.periodo}")
    except ObjectDoesNotExist:
        print("El periodo lectivo no existe")

def eliminar_logicamente_notas_periodo():
    periodo_id = 4
    try:
        periodo = Periodo.active_objects.get(pk=periodo_id)
        notas_a_eliminar = Nota.active_objects.filter(periodo_id=periodo_id)
        if notas_a_eliminar:
            for nota in notas_a_eliminar:
                nota.delete()
            print(f"Se han eliminado lógicamente todas las notas del período {periodo.periodo}.")
        else:
            print(f"No hay notas en el periodo {periodo.periodo}")
    except ObjectDoesNotExist:
        print("El periodo no existe")

def eliminar_fisicamente_notas_nota1_menora10():
    print("Eliminar fisicamente notas con la nota 1 menor a 10: ")
    notas_a_eliminar = DetalleNota.active_objects.filter(nota1__lt=10)
    cantidad_eliminada, _ = notas_a_eliminar.delete()
    if cantidad_eliminada > 0:
        print(f"Se han eliminado físicamente {cantidad_eliminada} notas con nota1 menor a 10.")
    else:
        print(f"No hay notas con notas 1 menores a 10")

# Sentencias CRUD:

# 60. Crear un registro de notas de un estudiante:
def crear_registro_notas_estudiante(estudiante_id):
    # Obtener el estudiante
    estudiante = Estudiante.objects.get(pk=estudiante_id)
    periodo = Periodo.objects.first() 
    profesor = Profesor.objects.first()  
    asignatura = Asignatura.objects.first()  

    # Crear la nota para el estudiante
    nota = Nota.objects.create(
        periodo=periodo,
        profesor=profesor,
        asignatura=asignatura,
        created=timezone.now(),
        updated=timezone.now()
    )
    # Crear detalles de la nota para el estudiante
    DetalleNota.objects.create(
        nota=nota,
        estudiante=estudiante,
        nota1=8.5,  # Aquí debes establecer el valor de la nota 1
        nota2=7.5,  # Aquí debes establecer el valor de la nota 2
        recuperacion=9.0,  # Aquí debes establecer el valor de la recuperación
        observacion="Nota registrada correctamente",
        created=timezone.now(),
        updated=timezone.now()
    )

    print(f'Notas registradas para el estudiante {estudiante.nombre}')

if __name__ == '__main__':
    insertar_datos_orm()
    buscar_y_mostrar_estudiantes('Est')#funciona
    buscar_y_mostrar_profesores('or')#modificar los datos quemados
    buscar_y_mostrar_asignaturas('10')#funciona
    buscar_y_mostrar_notas_por_nota1(8.0)#funciona
    buscar_y_mostrar_notas_por_nota2(9.0)#funciona
    buscar_y_mostrar_notas_por_recuperacion(8.5)#funciona
    buscar_y_mostrar_estudiantes_por_prefix_y_suffix('Est', '1')#funciona
    buscar_y_mostrar_asignaturas_por_contains_o_suffix('Asig', '5')#modificar los datpos quemados
    buscar_y_mostrar_profesores_por_nombre_no_contains('or')#funciona
    buscar_y_mostrar_notas_por_nota1_y_nota2(7.0, 8.0)#funciona
    buscar_y_mostrar_notas_por_recuperacion_is_null_o_nota2(9.0)#funciona
    seleccionar_notas_nota1_7a9()  #funciona
    seleccionar_notas_fuerade_6y8() #funciona
    seleccionar_recuperacion_notNone() #Funciona
    buscar_y_mostrar_notas_ultimo_anio()#funciona
    buscar_y_mostrar_notas_ultimo_mes()#modificar los datos quemados ejeplo estamos junio que presente las notas del mes pasado 
    buscar_y_mostrar_notas_ultimo_dia()#modificar los datos quemados ejemplo del dia entrio como sabado 
    buscar_y_mostrar_notas_antes_2023()#funciona
    buscar_y_mostrar_notas_marzo_cualquier_anio()#funciona
    buscar_y_mostrar_estudiantes_por_nombre_length(10)#modificar los datos quemados 
    buscar_y_mostrar_notas_por_nota1_y_nota2_gt(7.5)#modificar las notas que son mayores a 7.5
    buscar_y_mostrar_notas_por_recuperacion_y_nota1_gt_nota2()#funciona
    buscar_y_mostrar_notas_por_nota1_o_nota2(8.0, 7.5)#funciona
    buscar_y_mostrar_notas_por_recuperacion_gt_nota1_y_nota2()#funciona
    seleccionar_estudiantes_nota_recuperacion() #funciona
    profesores_con_asignatura_especifica() #no funciona
    asignatura_con_nota() #funciona
    asignatura_sin_notas() #funciona
    seleccionar_estudiantes_sin_nota_recuperacion() #funciona
    notas_promedio_mayor_8() #funciona
    notas_nota1_menora6_nota2_mayora7() #funciona
    notas_nota1_en_lista() #funciona
    notas_en_rango_id1a5() #funciona
    notas_recuperacion_noLista() #funciona
    suma_notas_de_estudiante() #funciona
    nota_maxima_estudiante() #funciona
    nota_minima_estudiante() #funciona
    notas_total_estudiante() #funciona
    promedio_notas_estudiante() #funciona 
    buscar_y_mostrar_notas_por_estudiante(1)  #Funciona, colocar con ID del estudiante
    buscar_y_mostrar_notas_por_periodo(1)  #funciona, colocar el ID del período
    buscar_y_mostrar_notas_por_asignatura_y_periodo(1, 1)  #funciona, colocar los IDs de asignatura y período
    buscar_y_mostrar_notas_por_profesor(1)  #funciona, colocar el ID del profesor
    buscar_y_mostrar_notas_estudiante_con_valor_mayor(3, 7.5)  #funciona, colocar el ID del estudiante y el valor deseado
    buscar_y_mostrar_notas_estudiante_ordenadas_por_periodo(3)  #no funciona, colocar el ID del estudiante
    mostrar_total_notas_estudiante(4)  #funciona, colocar el ID del estudiante
    mostrar_promedio_notas_estudiante_periodo(1, 1)  #funciona, colocar los IDs del estudiante y período
    buscar_y_mostrar_notas_con_observacion('Bueno')  #funciona, colocar la palabra que deseas que esté en el texto
    buscar_y_mostrar_notas_estudiante_ordenadas_por_asignatura(1)  #Funciona, colocar el ID del estudiante
    actualizar_nota1_para_menores(20)#funciona
    actualizar_nota2_para_menores(15)#funciona
    actualizar_recuperacion_para_menores(10)#funciona
    actualizar_observacion_para_aprobados()#funciona
    actualizar_notas_en_periodo('2023-2024')# NO funciona
    eliminar_notas_estudiante_fisica() #funciona
    eliminar_logicamente_notas_estudiantes() #funciona y actualiza el state a false
    eliminar_fisicamente_notas_de_periodo() #revisar
    eliminar_logicamente_notas_periodo() #revisar 
    eliminar_fisicamente_notas_nota1_menora10() #funciona
    crear_registro_notas_estudiante(5)#Revisar NO funciona 
