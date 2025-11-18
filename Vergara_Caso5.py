# datetime: Para manejar fechas y asignarlas automáticamente a los partidos
# timedelta: Para calcular diferencias de días entre rondas de partidos
# random: Para seleccionar canchas aleatoriamente al generar el fixture
from datetime import datetime, timedelta
import random

# Estas listas y diccionarios almacenan el estado del torneo en tiempo real
partidos_pendientes = []  # Partidos que aún no se han jugado
partidos_jugados = []     # Partidos ya completados con resultados
tabla_posiciones = {}     # Tabla de posiciones por equipo y deporte

# Muestra todas las opciones disponibles del sistema al usuario
def menu():
    print("\n---Bienvenido al sistema de gestión de torneos deportivos multi-disciplina.---")
    print("1. Registrar equipos.")
    print("2. Gestionar múltiples deportes (fútbol, baloncesto, voleibol).")
    print("3. Validar cupos por deporte (fútbol: 11-18, baloncesto: 5-12, voleibol: 6-14).")
    print("4. Generación de Fixture.")
    print("5. Registrar resultados de partido.")
    print("6. Registrar estadísticas individuales de cada jugador.")
    print("7. Ver Ranking de jugadores.")
    print("8. Mostrar tabla de posiciones.")
    print("9. Reportes del Torneo.")
    print("0. Salir.")

def buscar_jugador_por_id(id_jugador):
    #Buscamos un jugador por su ID en cualquiera de los tres deportes.
    for j in jugadores_futbol + jugadores_baloncesto + jugadores_voleibol:
        if j.get("ID") == id_jugador:
            return j
    return None

def buscar_equipo_por_nombre(nombre_equipo):
    #Localiza un equipo en la lista global de equipos por su nombre.
    for eq in equipos:
        if eq.get("Nombre") == nombre_equipo:
            return eq
    return None

def es_numero_camiseta_unico(equipo_nombre, numero, lista_jugadores):
    #Validamos que un número de camiseta no esté duplicado dentro de un equipo específico. De esa forma solo habrán camisetas únicas por equipo.
    return all(j.get("Número de Camiseta") != numero for j in lista_jugadores if j.get("Equipo") == equipo_nombre)

def agregar_jugador_generic(deporte):
    #Registramos un nuevo jugador en un equipo de un deporte específico (Fútbol, Baloncesto o Voleibol).

    id_jugador = int(input("Ingrese el ID del jugador: "))
    nombre_jugador = input("Ingrese el nombre del jugador: ")
    edad_jugador = int(input("Ingrese la edad del jugador: "))
    posicion_jugador = input("Ingrese la posición del jugador: ")
    numero_camiseta = int(input("Ingrese el número de camiseta: "))
    equipo_asignado = input("Ingrese el nombre del equipo al que pertenece el jugador: ")

    equipo_encontrado = next((eq for eq in equipos if eq["Nombre"] == equipo_asignado and eq["Deporte"] == deporte), None)
    if not equipo_encontrado:
        print(f"Equipo '{equipo_asignado}' no encontrado o no corresponde al deporte seleccionado.")
        return

    # contar jugadores actuales del equipo según deporte
    if deporte == 1:
        lista = jugadores_futbol
    elif deporte == 2:
        lista = jugadores_baloncesto
    else:
        lista = jugadores_voleibol

    num_jugadores_equipo = sum(1 for j in lista if j.get("Equipo") == equipo_asignado)
    _, max_jugadores = limite[deporte]
    if num_jugadores_equipo >= max_jugadores:
        print("No se pueden agregar más jugadores a ese equipo, se ha alcanzado el límite máximo para el deporte.")
        return

    existente = buscar_jugador_por_id(id_jugador)
    if existente:
        if existente.get("Equipo") != equipo_asignado:
            print(f"El jugador con ID '{id_jugador}' ya está registrado en el equipo '{existente.get('Equipo')}'. No puede pertenecer a otro equipo.")
        else:
            print(f"El jugador con ID '{id_jugador}' ya pertenece al equipo '{equipo_asignado}'.")
        return

    if not es_numero_camiseta_unico(equipo_asignado, numero_camiseta, lista):
        print(f"El número de camiseta '{numero_camiseta}' ya está en uso en el equipo '{equipo_asignado}'.")
        return

    nuevo_jugador = {
        "ID": id_jugador,
        "Nombre": nombre_jugador,
        "Edad": edad_jugador,
        "Posición": posicion_jugador,
        "Número de Camiseta": numero_camiseta,
        "Equipo": equipo_asignado
    }
    if deporte == 1:
        nuevo_jugador.update({"Goles": 0, "Asistencias": 0, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 0})
    if deporte == 2:
        nuevo_jugador.update({"Puntos": 0, "Rebotes": 0, "Asistencias": 0, "Robos": 0})
    if deporte == 3:
        nuevo_jugador.update({"Aces": 0, "Bloqueos": 0, "Recepciones": 0})

    lista.append(nuevo_jugador)
    equipo_encontrado["Jugadores"].append(id_jugador)
    print(f"Jugador '{nombre_jugador}' agregado al equipo '{equipo_asignado}'.")

def eliminar_jugador_generic(deporte):
    #Eliminar un jugador registrado de un equipo específico.
    id_eliminar = int(input("Ingrese el ID del jugador a eliminar: "))
    if deporte == 1:
        lista = jugadores_futbol
    elif deporte == 2:
        lista = jugadores_baloncesto
    else:
        lista = jugadores_voleibol

    for jugador in lista:
        if jugador.get("ID") == id_eliminar:
            equipo_jugador = jugador.get("Equipo")
            lista.remove(jugador)
            equipo_encontrado = next((eq for eq in equipos if eq["Nombre"] == equipo_jugador and eq["Deporte"] == deporte), None)
            if equipo_encontrado and id_eliminar in equipo_encontrado.get("Jugadores", []):
                equipo_encontrado["Jugadores"].remove(id_eliminar)
            print(f"Jugador con ID '{id_eliminar}' eliminado del equipo '{equipo_jugador}'.")
            return
    print(f"Jugador con ID '{id_eliminar}' no encontrado.")

def listar_jugadores_deporte(deporte):
    #Esto se encarga de mostrar todos los jugadores registrados en un deporte específico.
    if deporte == 1:
        lista = jugadores_futbol
        titulo = "Lista de jugadores de Fútbol:"
    elif deporte == 2:
        lista = jugadores_baloncesto
        titulo = "Lista de jugadores de Baloncesto:"
    else:
        lista = jugadores_voleibol
        titulo = "Lista de jugadores de Voleibol:"
    print(titulo)
    for jugador in lista:
        print(jugador)

def round_robin(teams):
    #Esto generar todas las rondas de un torneo "todos contra todos" (round-robin)
    if len(teams) == 0:
        return []
    if len(teams) % 2 == 1:
        teams.append(None)  # bye
    n = len(teams)
    rounds = []
    for i in range(n - 1):
        duelos = []
        for j in range(n // 2):
            t1 = teams[j]
            t2 = teams[n - 1 - j]
            if t1 is None or t2 is None:
                continue
            duelos.append((t1, t2))
        rounds.append(duelos)
        # rotación: mantener el primero, rotar el resto a la derecha
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
    return rounds

def generar_fixture_por_deporte(deporte, fecha_inicio, dias_entre_rondas=2, horarios=None):
    #Con esto se crea el calendario de partidos para un deporte específico.
    if horarios is None:
        horarios = ["10:00AM", "3:00PM", "7:00PM"]

    equipos_deporte = [eq["Nombre"] for eq in equipos if eq["Deporte"] == deporte]
    rounds = round_robin(equipos_deporte)
    partidos = []
    fecha_base = fecha_inicio

    for ronda_idx, ronda in enumerate(rounds):
        # slots por día = canchas * horarios
        slots_por_dia = len(canchas) * len(horarios)
        idx = 0
        dia_offset = 0
        while idx < len(ronda):
            fecha_actual = fecha_base + timedelta(days=dia_offset)
            # asignar tantos partidos como slots haya en este día
            for slot in range(slots_por_dia):
                if idx >= len(ronda):
                    break
                equipo1, equipo2 = ronda[idx]
                # seleccionar cancha aleatoriamente para distribuir partidos
                cancha = random.choice(canchas)[1]
                hora = horarios[(slot // len(canchas)) % len(horarios)]
                partido = {
                    "Deporte": deporte,
                    "Equipo 1": equipo1,
                    "Equipo 2": equipo2,
                    "Fecha": fecha_actual.strftime("%d-%m-%Y"),
                    "Hora": hora,
                    "Cancha": cancha
                }
                partidos.append(partido)
                idx += 1
            dia_offset += 1
        # después de completar la ronda, adelantar la fecha base para la siguiente ronda
        fecha_base = fecha_base + timedelta(days=dias_entre_rondas)

    return partidos

def generar_full_fixture(fecha_inicio=None, dias_entre_rondas=2, horarios=None):
    #Con esto se genera el fixture completo para TODOS los deportes del torneo.
    if fecha_inicio is None:
        fecha_inicio = datetime.now() + timedelta(days=1)
    full = []
    # generar por deporte usando fechas desplazadas para no mezclar rounds entre deportes
    desplazamiento = 0
    for deporte in deportes:
        inicio_deporte = fecha_inicio + timedelta(days=desplazamiento)
        partidos = generar_fixture_por_deporte(deporte, inicio_deporte, dias_entre_rondas, horarios)
        full.extend(partidos)
        # desplazar el inicio del siguiente deporte para intercalar calendarios
        desplazamiento += max(1, dias_entre_rondas)
    return full

def inicializar_estadisticas_jugadores(deporte):
    #Crea un diccionario de estadísticas inicial (en cero) para todos los jugadores de un deporte.
    # ESTADÍSTICAS FÚTBOL: Goles, Asistencias, Tarjetas Amarillas, Tarjetas Rojas
    # ESTADÍSTICAS BALONCESTO: Puntos, Rebotes, Asistencias, Robos
    # ESTADÍSTICAS VOLEIBOL: Aces, Bloqueos, Recepciones
    if deporte == 1:
        for jugador in jugadores_futbol:
            jugador["Estadísticas"] = {
                "Goles": 0,
                "Asistencias": 0,
                "Tarjetas Amarillas": 0,
                "Tarjetas Rojas": 0
            }
    # Baloncesto: Puntos, rebotes, asistencias y robos.
    elif deporte == 2:
        for jugador in jugadores_baloncesto:
            jugador["Estadísticas"] = {
                "Puntos": 0,
                "Rebotes": 0,
                "Asistencias": 0,
                "Robos": 0
            }
    # Voleibol: Aces, bloqueos y recepciones.
    elif deporte == 3:
        for jugador in jugadores_voleibol:
            jugador["Estadísticas"] = {
                "Aces": 0,
                "Bloqueos": 0,
                "Recepciones": 0
            }

def asegurar_estadisticas_jugador(jugador, deporte):
    #Garantiza que un jugador tenga la estructura correcta de estadísticas.
    if not jugador:
        return
    if "Estadísticas" in jugador:
        return
    if deporte == 1:
        Estadisticas = {}
        for k in ("Goles", "Asistencias", "Tarjetas Amarillas", "Tarjetas Rojas"):
            if k in jugador:
                Estadisticas[k] = jugador.pop(k)
            else:
                Estadisticas[k] = 0
        jugador["Estadísticas"] = Estadisticas
    elif deporte == 2:
        Estadisticas = {}
        for k in ("Puntos", "Rebotes", "Asistencias", "Robos"):
            if k in jugador:
                Estadisticas[k] = jugador.pop(k)
            else:
                Estadisticas[k] = 0
        jugador["Estadísticas"] = Estadisticas
    elif deporte == 3:
        Estadisticas = {}
        for k in ("Aces", "Bloqueos", "Recepciones"):
            if k in jugador:
                Estadisticas[k] = jugador.pop(k)
            else:
                Estadisticas[k] = 0
        jugador["Estadísticas"] = Estadisticas

def registrar_estadisticas_jugador(deporte):
    #Permite sumar estadísticas a un jugador después de un partido, según el deporte.
    id_jugador = int(input("Ingrese el ID del jugador para registrar estadísticas: "))
    if deporte == 1:
        lista = jugadores_futbol
    elif deporte == 2:
        lista = jugadores_baloncesto
    else:
        lista = jugadores_voleibol
    jugador_encontrado = next((j for j in lista if j["ID"] == id_jugador), None)
    if not jugador_encontrado:
        print(f"Jugador con ID '{id_jugador}' no encontrado en el deporte seleccionado.")
        return
    #Esto asegura que exista la clave 'Estadísticas'.
    asegurar_estadisticas_jugador(jugador_encontrado, deporte)
    if deporte == 1:
        goles = int(input("Ingrese la cantidad de goles a sumar: "))
        asistencias = int(input("Ingrese la cantidad de asistencias a sumar: "))
        tarjetas_amarillas = int(input("Ingrese la cantidad de tarjetas amarillas a sumar: "))
        tarjetas_rojas = int(input("Ingrese la cantidad de tarjetas rojas a sumar: "))
        jugador_encontrado["Estadísticas"]["Goles"] += goles
        jugador_encontrado["Estadísticas"]["Asistencias"] += asistencias
        jugador_encontrado["Estadísticas"]["Tarjetas Amarillas"] += tarjetas_amarillas
        jugador_encontrado["Estadísticas"]["Tarjetas Rojas"] += tarjetas_rojas

    elif deporte == 2:
        puntos = int(input("Ingrese la cantidad de puntos a sumar: "))
        rebotes = int(input("Ingrese la cantidad de rebotes a sumar: "))
        asistencias = int(input("Ingrese la cantidad de asistencias a sumar: "))
        robos = int(input("Ingrese la cantidad de robos a sumar: "))
        jugador_encontrado["Estadísticas"]["Puntos"] += puntos
        jugador_encontrado["Estadísticas"]["Rebotes"] += rebotes
        jugador_encontrado["Estadísticas"]["Asistencias"] += asistencias
        jugador_encontrado["Estadísticas"]["Robos"] += robos

    else:
        aces = int(input("Ingrese la cantidad de aces a sumar: "))
        bloqueos = int(input("Ingrese la cantidad de bloqueos a sumar: "))
        recepciones = int(input("Ingrese la cantidad de recepciones a sumar: "))
        jugador_encontrado["Estadísticas"]["Aces"] += aces
        jugador_encontrado["Estadísticas"]["Bloqueos"] += bloqueos
        jugador_encontrado["Estadísticas"]["Recepciones"] += recepciones
    print(f"Estadísticas actualizadas para el jugador '{jugador_encontrado['Nombre']}'.")

def mostrar_ranking_jugadores(deporte):
    #Se muestra el ranking de mejores jugadores por categoría dentro de cada deporte.
    #SALIDA FÚTBOL: Top Goleadores, Top Asistencias, Mayor Tarjetas Amarillas, Mayor Tarjetas Rojas.
    #SALIDA BALONCESTO: Top Puntos, Top Rebotes, Top Asistencias, Top Robos.
    #SALIDA VOLEIBOL: Top Aces, Top Bloqueos, Top Recepciones.
    print("--- Ranking de Jugadores ---")
    print("Seleccione el deporte para ver el ranking:")
    print("1. Fútbol")
    print("2. Baloncesto")
    print("3. Voleibol")
    deporte = int(input("Ingrese el número correspondiente al deporte: "))
    if deporte == 1:
        # Normalizar estadísticas de fútbol
        for j in jugadores_futbol:
            asegurar_estadisticas_jugador(j, 1)
        goleadores = sorted(jugadores_futbol, key=lambda j: j["Estadísticas"]["Goles"], reverse=True)
        print("\n""Ranking de Goleadores de Fútbol:")
        for idx, jugador in enumerate(goleadores, start=1):
            print(f"{idx}. {jugador['Nombre']} - Goles: {jugador['Estadísticas']['Goles']}")

        print("\n""Ranking de Asistencias de Fútbol:")
        asistencias = sorted(jugadores_futbol, key=lambda j: j["Estadísticas"]["Asistencias"], reverse=True)
        for idx, jugador in enumerate(asistencias, start=1):
            print(f"{idx}. {jugador['Nombre']} - Asistencias: {jugador['Estadísticas']['Asistencias']}")

        print("\n Más Tarjetas Amarillas:")
        tarjetas_amarillas = sorted(jugadores_futbol, key=lambda j: j["Estadísticas"]["Tarjetas Amarillas"], reverse=True)
        for idx, jugador in enumerate(tarjetas_amarillas, start=1):
            print(f"{idx}. {jugador['Nombre']} - Tarjetas Amarillas: {jugador['Estadísticas']['Tarjetas Amarillas']}")
        
        print("\n Más Tarjetas Rojas:")
        tarjetas_rojas = sorted(jugadores_futbol, key=lambda j: j["Estadísticas"]["Tarjetas Rojas"], reverse=True)
        for idx, jugador in enumerate(tarjetas_rojas, start=1):
            print(f"{idx}. {jugador['Nombre']} - Tarjetas Rojas: {jugador['Estadísticas']['Tarjetas Rojas']}")

    elif deporte == 2:
        # Normalizar estadísticas de baloncesto
        for j in jugadores_baloncesto:
            asegurar_estadisticas_jugador(j, 2)
        print ("\n""Ranking de Puntos de Baloncesto:")
        puntos = sorted(jugadores_baloncesto, key=lambda j: j["Estadísticas"]["Puntos"], reverse=True)
        for idx, jugador in enumerate(puntos, start=1):
            print(f"{idx}. {jugador['Nombre']} - Puntos: {jugador['Estadísticas']['Puntos']}")

        print ("\n""Ranking de Rebotes de Baloncesto:")
        rebotes = sorted(jugadores_baloncesto, key=lambda j: j["Estadísticas"]["Rebotes"], reverse=True)
        for idx, jugador in enumerate(rebotes, start=1):
            print(f"{idx}. {jugador['Nombre']} - Rebotes: {jugador['Estadísticas']['Rebotes']}")
       
        print ("\n""Ranking de Asistencias de Baloncesto:")
        asistencias = sorted(jugadores_baloncesto, key=lambda j: j["Estadísticas"]["Asistencias"], reverse=True)
        for idx, jugador in enumerate(asistencias, start=1):
            print(f"{idx}. {jugador['Nombre']} - Asistencias: {jugador['Estadísticas']['Asistencias']}")

        print ("\n""Ranking de Robos de Baloncesto:")
        robos = sorted(jugadores_baloncesto, key=lambda j: j["Estadísticas"]["Robos"], reverse=True)
        for idx, jugador in enumerate(robos, start=1):
            print(f"{idx}. {jugador['Nombre']} - Robos: {jugador['Estadísticas']['Robos']}")

    else:
        # Normalizar estadísticas de voleibol
        for j in jugadores_voleibol:
            asegurar_estadisticas_jugador(j, 3)
        print ("\n""Ranking de Aces de Voleibol:")
        aces = sorted(jugadores_voleibol, key=lambda j: j["Estadísticas"]["Aces"], reverse=True)
        for idx, jugador in enumerate(aces, start=1):
            print(f"{idx}. {jugador['Nombre']} - Aces: {jugador['Estadísticas']['Aces']}")

        print ("\n""Ranking de Bloqueos de Voleibol:")
        bloqueos = sorted(jugadores_voleibol, key=lambda j: j["Estadísticas"]["Bloqueos"], reverse=True)
        for idx, jugador in enumerate(bloqueos, start=1):
            print(f"{idx}. {jugador['Nombre']} - Bloqueos: {jugador['Estadísticas']['Bloqueos']}")

        print ("\n""Ranking de Recepciones de Voleibol:")
        recepciones = sorted(jugadores_voleibol, key=lambda j: j["Estadísticas"]["Recepciones"], reverse=True)
        for idx, jugador in enumerate(recepciones, start=1):
            print(f"{idx}. {jugador['Nombre']} - Recepciones: {jugador['Estadísticas']['Recepciones']}")

def validar_jugadores_partido(partido):
    #Validamos que ambos equipos de un partido cumplan el mínimo de jugadores requerido.
    deporte = partido.get("Deporte")
    equipo1 = partido.get("Equipo 1")
    equipo2 = partido.get("Equipo 2")
    if deporte == 1:
        min_jug, _ = limite[1]
        n1 = sum(1 for j in jugadores_futbol if j.get("Equipo") == equipo1)
        n2 = sum(1 for j in jugadores_futbol if j.get("Equipo") == equipo2)
    elif deporte == 2:
        min_jug, _ = limite[2]
        n1 = sum(1 for j in jugadores_baloncesto if j.get("Equipo") == equipo1)
        n2 = sum(1 for j in jugadores_baloncesto if j.get("Equipo") == equipo2)
    else:
        min_jug, _ = limite[3]
        n1 = sum(1 for j in jugadores_voleibol if j.get("Equipo") == equipo1)
        n2 = sum(1 for j in jugadores_voleibol if j.get("Equipo") == equipo2)

    return n1 >= min_jug and n2 >= min_jug

def actualizar_tabla_posiciones(equipo_nombre, puntos, pj, pg, pe, pp, pf, pc):
    #Esto crea o actualiza la entrada de un equipo en la tabla de posiciones.
    if equipo_nombre not in tabla_posiciones:
        info_equipo = next((eq for eq in equipos if eq["Nombre"] == equipo_nombre), None)
        deporte_equipo = info_equipo["Deporte"] if info_equipo else None
        tabla_posiciones[equipo_nombre] = {
            "Deporte": deporte_equipo,
            "Puntos": 0,
            "Partidos Jugados": 0,
            "Ganados": 0,
            "Empatados": 0,
            "Perdidos": 0,
            "Puntos a Favor": 0,
            "Puntos en Contra": 0,
            "Diferencia": 0
        }

    entrada = tabla_posiciones[equipo_nombre]
    entrada["Puntos"] += puntos
    entrada["Partidos Jugados"] += pj
    entrada["Ganados"] += pg
    entrada["Empatados"] += pe
    entrada["Perdidos"] += pp
    entrada["Puntos a Favor"] += pf
    entrada["Puntos en Contra"] += pc
    entrada["Diferencia"] = entrada["Puntos a Favor"] - entrada["Puntos en Contra"]

def mostrar_tabla_posiciones():
    #Muestrar toda la tabla de posiciones ordenada de un deporte seleccionado.
    print("\n---Tabla de Posiciones---")

    deporte_seleccion = int(input("Seleccione el deporte para ver la tabla de posiciones (1: Fútbol, 2: Baloncesto, 3: Voleibol): "))
    
    # Si no hay entradas en tabla_posiciones, inicializar desde la lista `equipos`
    if not tabla_posiciones:
        for eq in equipos:
            tabla_posiciones.setdefault(eq["Nombre"], {
                "Deporte": eq["Deporte"],
                "Puntos": 0,
                "Partidos Jugados": 0,
                "Ganados": 0,
                "Empatados": 0,
                "Perdidos": 0,
                "Puntos a Favor": 0,
                "Puntos en Contra": 0,
                "Diferencia": 0
            })

    equipos_ordenados = []
    for nombre_equipo, Estadisticas in tabla_posiciones.items():
        if Estadisticas.get("Deporte") == deporte_seleccion:
            Estadisticas["Equipo"] = nombre_equipo
            equipos_ordenados.append(Estadisticas)

    if not equipos_ordenados:
        print("No hay equipos registrados para este deporte.")
        return

    #Ordenar por puntos, diferencia y goles a favor
    tabla_ordenada = sorted(equipos_ordenados, key=lambda eq: (eq["Puntos"], eq["Diferencia"], eq["Puntos a Favor"]), reverse=True) #Ordenamos de menor a mayor.
    print(f"\nTabla de Posiciones - Deporte {deporte_seleccion}")
    print("-" * 80)
    print(f"{'Equipo':<20} {'Puntos':<8} {'PJ':<4} {'PG':<4} {'PE':<4} {'PP':<4} {'PF':<6} {'PC':<6} {'Dif':<6}")
    print("-" * 80)

    for eq in tabla_ordenada:
        print(f"{eq['Equipo']:<20} {eq['Puntos']:<8} {eq['Partidos Jugados']:<4} {eq['Ganados']:<4} {eq['Empatados']:<4} {eq['Perdidos']:<4} {eq['Puntos a Favor']:<6} {eq['Puntos en Contra']:<6} {eq['Diferencia']:<6}\n")

def registrar_resultado_partido():
    #Esto se encarga de registrar el resultado final de un partido pendiente.
    if not partidos_pendientes:
        print("No hay partidos pendientes para registrar resultados.")
        print("Genere el fixture primero (opción 4 del menú).")
        return

    print("\n---Registrar Resultado de Partido---")
    print("Seleccione el partido al que deseas registrar un resultado.")

    for i, p in enumerate(partidos_pendientes):
        print(f" {i+1}. [{p['Fecha']} {p['Hora']}] {p['Equipo 1']} vs {p['Equipo 2']} (Deporte: {p['Deporte']})")

    try:
        idx_seleccion = int(input("Seleccione el N° de partido (0 para cancelar): "))
        if idx_seleccion == 0:
            return
        partido_seleccionado = partidos_pendientes[idx_seleccion - 1]
    except (ValueError, IndexError):
        print("Selección inválida. Intente de nuevo.")
        return

    print(f"\nRegistrando resultado para: {partido_seleccionado['Equipo 1']} vs {partido_seleccionado['Equipo 2']}")

    # Validamos que solo jueguen jugadores inscritos y confirmamos que los equipos tengan el mínimo de jugadores.
    if not validar_jugadores_partido(partido_seleccionado):
        print("El partido no se puede registrar hasta que ambos equipos cumplan el mínimo de jugadores.")
        return

    #Pasamos al registro de resultados de partidos.
    try:
        # Para Fútbol (Deporte 1) y Baloncesto (Deporte 2) pedimos marcador directo
        if partido_seleccionado['Deporte'] == 1 or partido_seleccionado['Deporte'] == 2:
            puntaje_1 = int(input(f"Resultado final - {partido_seleccionado['Equipo 1']}: "))
            puntaje_2 = int(input(f"Resultado final - {partido_seleccionado['Equipo 2']}: "))

        #Para Voleibol (Deporte 3) preguntamos por sets.
        elif partido_seleccionado['Deporte'] == 3:
            print("Resultado (sets ganados) - Voleibol. Determine el ganador por sets.")
            sets_1 = int(input(f"Sets ganados - {partido_seleccionado['Equipo 1']}: "))
            sets_2 = int(input(f"Sets ganados - {partido_seleccionado['Equipo 2']}: "))
            # Usamos los sets como 'puntaje' para determinar el ganador
            puntaje_1 = sets_1
            puntaje_2 = sets_2

    except ValueError:
        print("Entrada de resultado inválida. Debe ser un número.")
        return

    #Determinamos al ganador y actualizamos las estadísticas.
    puntos1, pg1, pe1, pp1 = 0, 0, 0, 0
    puntos2, pg2, pe2, pp2 = 0, 0, 0, 0

    if puntaje_1 > puntaje_2:  #Gana el Equipo 1
        puntos1 = 3
        pg1 = 1
        pp2 = 1
    elif puntaje_1 < puntaje_2:  #Gana el Equipo 2
        puntos2 = 3
        pg2 = 1
        pp1 = 1
    else:  # Empate (Solo aplica a Fútbol)
        if partido_seleccionado['Deporte'] == 1:
            puntos1 = 1
            puntos2 = 1
            pe1 = 1
            pe2 = 1
        else:
            print(f"Error: {partido_seleccionado['Deporte']} no permite empates. Ingrese el resultado de desempate.")
            return

    #Actualizamos la tabla para ambos equipos.
    actualizar_tabla_posiciones(partido_seleccionado['Equipo 1'], puntos1, 1, pg1, pe1, pp1, puntaje_1, puntaje_2)
    actualizar_tabla_posiciones(partido_seleccionado['Equipo 2'], puntos2, 1, pg2, pe2, pp2, puntaje_2, puntaje_1)

    #Movemos el partido de 'pendientes' a 'jugados'.
    partido_completado = partidos_pendientes.pop(idx_seleccion - 1)

    #Guardamos el resultado en el diccionario del partido.
    partido_completado['Resultado'] = f"{puntaje_1} - {puntaje_2}"
    partido_completado['Ganador'] = partido_seleccionado['Equipo 1'] if puntaje_1 > puntaje_2 else (partido_seleccionado['Equipo 2'] if puntaje_2 > puntaje_1 else "Empate")
    partidos_jugados.append(partido_completado)

    print(f"\nPartido registrado exitosamente: {partido_seleccionado['Equipo 1']} {puntaje_1} - {puntaje_2} {partido_seleccionado['Equipo 2']}")
    print("\n¡PARTIDO REGISTRADO EXITOSAMENTE!")
    print("Utilice la opción 6 para sumar las estadísticas a los jugadores que participaron en el partido.")

def reporte_fixture_completo():
    #Esto nos muestra la lista completa de partidos jugados y pendientes.
    print("\n---Reporte Completo del Fixture---")
    print("\n---Partidos Pendientes---")
    if partidos_pendientes:
        for p in partidos_pendientes:
            print(f"[{p['Fecha']} {p['Hora']}] {p['Equipo 1']} vs {p['Equipo 2']} (Deporte: {p['Deporte']})")
    else:
        print("No hay partidos pendientes.")

    print("\n---Partidos Jugador y Resultados---")
    if partidos_jugados:
        for p in partidos_jugados:
            print(f"[{p['Fecha']} {p['Hora']}] {p['Equipo 1']} {p.get('Resultado', '')} {p['Equipo 2']} - Ganador: {p.get('Ganador', 'N/A')} (Deporte: {p['Deporte']})")
    else:
        print("No hay partidos jugados.")

def reporte_top_ofensivo_defensivo():
    #Mostrar el top 5 de equipos más ofensivos y con mejor defensa por deporte.
    print("\n---Reporte de equipos con mejor rendimiento ofensivo y defensivo---")

    deporte_seleccion = int(input("Seleccione el deporte para ver el reporte (1: Fútbol, 2: Baloncesto, 3: Voleibol): "))
    equipos_ordenados = [(nombre, Estadisticas) for nombre, Estadisticas in tabla_posiciones.items() if Estadisticas.get("Deporte") == deporte_seleccion]
    if not equipos_ordenados:
        print("No hay equipos registrados para este deporte.")
    
    top_ofensivo = sorted(equipos_ordenados, key=lambda item: item[1]["Puntos a Favor"], reverse=True)
    top_defensivo = sorted(equipos_ordenados, key=lambda item: item[1]["Puntos en Contra"])
    if top_ofensivo:
        mejor_ofensivo = top_ofensivo[0]
        print(f"\nEquipo más ofensivo en Deporte {deporte_seleccion}: {mejor_ofensivo[0]} con {mejor_ofensivo[1]['Puntos a Favor']} puntos a favor.")

        print(f"\n---Top equipo más goleador/anotador - Deporte {deporte_seleccion}---")
        for idx, (nombre, Estadisticas) in enumerate(top_ofensivo[:5], start=1):
            print(f"{idx}. {nombre} - Puntos a Favor: {Estadisticas['Puntos a Favor']}")

        print(f"\n---Top equipo con mejor defensa - Deporte {deporte_seleccion}---")
        for idx, (nombre, Estadisticas) in enumerate(top_defensivo[:5], start=1):
            print(f"{idx}. {nombre} - Puntos en Contra: {Estadisticas['Puntos en Contra']}")

def reporte_proximos_partidos():
    #Mostramos todos los partidos pendientes de un equipo específico.
    print("\n---Reporte de Próximos Partidos de un Equipo---")
    nombre_equipo = input("Ingrese el nombre del equipo: ")

    proximo = [
        p for p in partidos_pendientes
        if p['Equipo 1'] == nombre_equipo or p['Equipo 2'] == nombre_equipo
    ]
    if not proximo:
        print(f"No hay próximos partidos registrados para el equipo '{nombre_equipo}'.")
        return

    print(f"\n---Próximos partidos de: {nombre_equipo}---")
    for p in proximo:
        rival = p['Equipo 2'] if p['Equipo 1'] == nombre_equipo else p['Equipo 1']
        print(f"[{p['Fecha']} {p['Hora']}] vs {rival} en {p['Cancha']} (Deporte: {p['Deporte']})")

def reporte_historial_enfrentamientos():
    #Muestra el historial de todos los partidos jugados entre dos equipos específicos.
    equipo_1 = input("\nIngrese el nombre del equipo 1: ")
    equipo_2 = input("\nIngrese el nombre del equipo 2: ")

    historial = [
        p for p in partidos_jugados
        if (p['Equipo 1'] == equipo_1 and p['Equipo 2'] == equipo_2) or (p['Equipo 1'] == equipo_2 and p['Equipo 2'] == equipo_1)
    ]

    if not historial:
        print(f"No hay historial de enfrentamientos entre '{equipo_1}' y '{equipo_2}'.")
        return
    
    print(f"\n---Historial de enfrentamientos entre {equipo_1} y {equipo_2}---")
    
    victorias_eq1 = 0
    victorias_eq2 = 0

    for p in historial:
        if p['Ganador'] == equipo_1:
            victorias_eq1 += 1
            resultado = f"{p['Resultado']} - Ganador: {equipo_1}"
        elif p['Ganador'] == equipo_2:
            victorias_eq2 += 1
            resultado = f"{p['Resultado']} - Ganador: {equipo_2}"
        else:
            resultado = f"{p['Resultado']} - Empate"

        print(f"Resumen: [{p['Fecha']}] {p['Hora']}] {p['Equipo 1']} vs {p['Equipo 2']} - {resultado}")

def reporte_prediccion_campeon():
    #Se encarga de predecir el campeón probable de un deporte basado en estadísticas actuales.
    print("\n---Predicción de Campeón por Deporte (Basada en Puntos)---")
    
    deporte_seleccion = int(input("Seleccione el deporte para ver la predicción (1: Fútbol, 2: Baloncesto, 3: Voleibol): "))
    if deporte_seleccion not in [1, 2, 3]:
        print("Deporte inválido.")
        return
    
    equipos_ordenados = [(nombre, Estadisticas) for nombre, Estadisticas in tabla_posiciones.items() if Estadisticas.get("Deporte") == deporte_seleccion]
    if not equipos_ordenados:
        print("No hay equipos registrados para este deporte.")
        return

    tabla_ordenada = sorted(equipos_ordenados, key=lambda item: (item[1]["Puntos"], item[1]["Diferencia"], item[1]['Puntos a Favor']), reverse=True)
    if tabla_ordenada:
        campeon_predicho = tabla_ordenada[0][0]
        puntos = tabla_ordenada[0][1]["Puntos"]
        print(f"\nBasado en las estadísticas actuales, el campeón predicho es: {campeon_predicho} con {puntos} puntos.")
    else:
        print("No se pudo determinar un campeón predicho.")

def mostrar_reportes_torneo():
    #Esto simplemente es un menú de submenu para acceder a todos los reportes analíticos del torneo.
    while True:
        print("\n---Menú de Reportes del Torneo---")
        print("1. Reporte completo del Fixture (Jugados y Pendientes)")
        print("2. Equipos más goleadores/anotadores y con mejor defensa.")
        print("3. Próximos partidos de un equipo en específico.")
        print("4. Historial de enfrentamientos entre dos equipos.")
        print("5. Predicción del campeón (Basada en la tabla actual).")
        print("6. Volver al menú principal.")

        opcion_reporte = input("Seleccione una opción de reporte (1-6): ")

        if opcion_reporte == '1':
            reporte_fixture_completo()
        elif opcion_reporte == '2':
            reporte_top_ofensivo_defensivo()
        elif opcion_reporte == '3':
            reporte_proximos_partidos()
        elif opcion_reporte == '4':
            reporte_historial_enfrentamientos()
        elif opcion_reporte == '5':
            reporte_prediccion_campeon()
        elif opcion_reporte == '6':
            break

#Esta es una lista de los datos y estadísticas de todos los jugadores.

#FÚTBOL: Incluye goles, asistencias, tarjetas amarillas, tarjetas rojas
jugadores_futbol = [{ "ID": 1, "Nombre": "Juan Perez", "Edad": 25, "Posición": "Delantero", "Número de Camiseta": 9, "Equipo": 'Atlético Nacional', "Goles": 4, "Asistencias": 5, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 2},
             { "ID": 2, "Nombre": "Carlos Gómez", "Edad": 22, "Posición": "Central", "Número de Camiseta": 7, "Equipo": 'Atlético Nacional', "Goles": 2, "Asistencias": 3, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 1},
             { "ID": 3, "Nombre": "Luis Martínez", "Edad": 28, "Posición": "Central", "Número de Camiseta": 5, "Equipo": 'Atlético Nacional', "Goles": 1, "Asistencias": 4, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 0},
             { "ID": 4, "Nombre": "Pedro Rodríguez", "Edad": 30, "Posición": "Portero", "Número de Camiseta": 1, "Equipo": 'Atlético Nacional', "Goles": 0, "Asistencias": 0, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 5, "Nombre": "Javier Hernández", "Edad": 26, "Posición": "Defensa", "Número de Camiseta": 6, "Equipo": 'Atlético Nacional', "Goles": 3, "Asistencias": 2, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 1},
             { "ID": 6, "Nombre": "Fernando López", "Edad": 29, "Posición": "Delantero", "Número de Camiseta": 15, "Equipo": 'Atlético Nacional', "Goles": 5, "Asistencias": 1, "Tarjetas Amarillas": 3, "Tarjetas Rojas": 0},
             { "ID": 7, "Nombre": "Diego Maradona", "Edad": 23, "Posición": "Mediocampista", "Número de Camiseta": 3, "Equipo": 'Atlético Nacional', "Goles": 3 , "Asistencias": 4, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 1},
             { "ID": 8, "Nombre": "Sergio Ramírez", "Edad": 27, "Posición": "Central", "Número de Camiseta": 12, "Equipo": 'Atlético Nacional', "Goles": 2, "Asistencias": 3, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 9, "Nombre": "Andrés Iniesta", "Edad": 24, "Posición": "Mediocampista", "Número de Camiseta": 8, "Equipo": 'Atlético Nacional', "Goles": 4, "Asistencias": 6, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 0},
             { "ID": 10, "Nombre": "Raúl González", "Edad": 28, "Posición": "Defensa", "Número de Camiseta": 4, "Equipo": 'Atlético Nacional', "Goles": 1, "Asistencias": 2, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 1},
             { "ID": 11, "Nombre": "David Villa", "Edad": 26, "Posición": "Delantero", "Número de Camiseta": 10, "Equipo": 'Atlético Nacional', "Goles": 6, "Asistencias": 3, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 12, "Nombre": "Xavi Hernández", "Edad": 29, "Posición": "Mediocampista", "Número de Camiseta": 14, "Equipo": 'Atlético Nacional', "Goles": 2, "Asistencias": 5, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 0},
             { "ID": 13, "Nombre": "César Sánchez", "Edad": 31, "Posición": "Portero", "Número de Camiseta": 13, "Equipo": 'Deportivo Cali', "Goles": 0, "Asistencias": 0, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 14, "Nombre": "Roberto Carlos", "Edad": 32, "Posición": "Defensa", "Número de Camiseta": 2, "Equipo": 'Deportivo Cali', "Goles": 1, "Asistencias": 2, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 1},
             { "ID": 15, "Nombre": "Ronaldinho", "Edad": 27, "Posición": "Delantero", "Número de Camiseta": 11, "Equipo": 'Deportivo Cali', "Goles": 5, "Asistencias": 4, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 16, "Nombre": "Kaká", "Edad": 25, "Posición": "Mediocampista", "Número de Camiseta": 15, "Equipo": 'Deportivo Cali', "Goles": 3, "Asistencias": 5, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 0},
             { "ID": 17, "Nombre": "Neymar Jr.", "Edad": 24, "Posición": "Delantero", "Número de Camiseta": 10, "Equipo": 'Deportivo Cali', "Goles": 7, "Asistencias": 6, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 18, "Nombre": "Zlatan Ibrahimović", "Edad": 29, "Posición": "Delantero", "Número de Camiseta": 9, "Equipo": 'Deportivo Cali', "Goles": 6, "Asistencias": 3, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 1},
             { "ID": 19, "Nombre": "Andrés Escobar", "Edad": 28, "Posición": "Defensa", "Número de Camiseta": 4, "Equipo": 'Deportivo Cali', "Goles": 0, "Asistencias": 1, "Tarjetas Amarillas": 3, "Tarjetas Rojas": 0},
             { "ID": 20, "Nombre": "Freddy Rincón", "Edad": 30, "Posición": "Mediocampista", "Número de Camiseta": 8, "Equipo": 'Deportivo Cali', "Goles": 2, "Asistencias": 4, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 21, "Nombre": "James Rodríguez", "Edad": 26, "Posición": "Mediocampista", "Número de Camiseta": 11, "Equipo": 'Deportivo Cali', "Goles": 8, "Asistencias": 7, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 0},
             { "ID": 22, "Nombre": "Falcao García", "Edad": 27, "Posición": "Delantero", "Número de Camiseta": 7, "Equipo": 'Deportivo Cali', "Goles": 9, "Asistencias": 2, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 23, "Nombre": "Carlos Bacca", "Edad": 28, "Posición": "Delantero", "Número de Camiseta": 9, "Equipo": 'Deportivo Cali', "Goles": 5, "Asistencias": 3, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 1},
             { "ID": 24, "Nombre": "Radamel Falcao", "Edad": 29, "Posición": "Delantero", "Número de Camiseta": 19, "Equipo": 'Deportivo Cali', "Goles": 10, "Asistencias": 4, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 25, "Nombre": "Juan Cuadrado", "Edad": 25, "Posición": "Mediocampista", "Número de Camiseta": 16, "Equipo": 'Deportivo Cali', "Goles": 4, "Asistencias": 6, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 0},
             { "ID": 26, "Nombre": "David Ospina", "Edad": 27, "Posición": "Portero", "Número de Camiseta": 1, "Equipo": 'Deportivo Cali', "Goles": 0, "Asistencias": 0, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 27, "Nombre": "Yerry Mina", "Edad": 24, "Posición": "Defensa", "Número de Camiseta": 5, "Equipo": 'Millonarios', "Goles": 2, "Asistencias": 1, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 0},
             { "ID": 28, "Nombre": "Duván Zapata", "Edad": 26, "Posición": "Delantero", "Número de Camiseta": 9, "Equipo": 'Millonarios', "Goles": 7, "Asistencias": 3, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 1},
             { "ID": 29, "Nombre": "Wilmar Barrios", "Edad": 25, "Posición": "Mediocampista", "Número de Camiseta": 8, "Equipo": 'Millonarios', "Goles": 1, "Asistencias": 4, "Tarjetas Amarillas": 3, "Tarjetas Rojas": 0},
             { "ID": 30, "Nombre": "Santiago Arias", "Edad": 27, "Posición": "Defensa", "Número de Camiseta": 2, "Equipo": 'Millonarios', "Goles": 0, "Asistencias": 2, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 1},
             { "ID": 31, "Nombre": "Mateus Uribe", "Edad": 28, "Posición": "Mediocampista", "Número de Camiseta": 6, "Equipo": 'Millonarios', "Goles": 3, "Asistencias": 5, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 32, "Nombre": "Luis Díaz", "Edad": 22, "Posición": "Delantero", "Número de Camiseta": 11, "Equipo": 'Millonarios', "Goles": 6, "Asistencias": 4, "Tarjetas Amarillas": 0, "Tarjetas Rojas": 0},
             { "ID": 33, "Nombre": "Camilo Vargas", "Edad": 29, "Posición": "Portero", "Número de Camiseta": 1, "Equipo": 'Millonarios', "Goles": 0, "Asistencias": 0, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 34, "Nombre": "Jhon Córdoba", "Edad": 26, "Posición": "Delantero", "Número de Camiseta": 10, "Equipo": 'Millonarios', "Goles": 8, "Asistencias": 2, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 1},
             { "ID": 35, "Nombre": "Daniel Torres", "Edad": 30, "Posición": "Defensa", "Número de Camiseta": 4, "Equipo": 'Millonarios', "Goles": 1, "Asistencias": 3, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 0},
             { "ID": 36, "Nombre": "Andrés Cadavid", "Edad": 31, "Posición": "Defensa", "Número de Camiseta": 3, "Equipo": 'Millonarios', "Goles": 0, "Asistencias": 1, "Tarjetas Amarillas": 3, "Tarjetas Rojas": 1},
             { "ID": 37, "Nombre": "Javier Reina", "Edad": 27, "Posición": "Mediocampista", "Número de Camiseta": 14, "Equipo": 'Millonarios', "Goles": 2, "Asistencias": 4, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},
             { "ID": 38, "Nombre": "Helibelton Palacios", "Edad": 24, "Posición": "Defensa", "Número de Camiseta": 5, "Equipo": 'Millonarios', "Goles": 0, "Asistencias": 2, "Tarjetas Amarillas": 2, "Tarjetas Rojas": 0},
             { "ID": 39, "Nombre": "Brayan Angulo", "Edad": 28, "Posición": "Delantero", "Número de Camiseta": 7, "Equipo": 'Millonarios', "Goles": 4, "Asistencias": 3, "Tarjetas Amarillas": 1, "Tarjetas Rojas": 0},]

#BALONCESTO: Incluye puntos, rebotes, asistencias, robos
jugadores_baloncesto = [{ "ID": 1, "Nombre": "Miguel Sánchez", "Edad": 27, "Posición": "Alero", "Número de Camiseta": 11, "Equipo": 'Bucos de Santander', "Puntos": 150, "Rebotes": 80, "Asistencias": 40, "Robos": 20},
                       { "ID": 2, "Nombre": "Luis Fernández", "Edad": 24, "Posición": "Base", "Número de Camiseta": 3, "Equipo": 'Bucos de Santander', "Puntos": 120, "Rebotes": 50, "Asistencias": 70, "Robos": 25},
                       { "ID": 3, "Nombre": "Javier Martínez", "Edad": 29, "Posición": "Escolta", "Número de Camiseta": 5, "Equipo": 'Bucos de Santander', "Puntos": 130, "Rebotes": 60, "Asistencias": 50, "Robos": 30},
                       { "ID": 4, "Nombre": "Carlos López", "Edad": 26, "Posición": "Pívot", "Número de Camiseta": 15, "Equipo": 'Bucos de Santander', "Puntos": 140, "Rebotes": 90, "Asistencias": 30, "Robos": 15},
                       { "ID": 5, "Nombre": "Sergio Gómez", "Edad": 28, "Posición": "Ala-pívot", "Número de Camiseta": 7, "Equipo": 'Bucos de Santander', "Puntos": 110, "Rebotes": 70, "Asistencias": 20, "Robos": 10},
                       { "ID": 6, "Nombre": "Diego Torres", "Edad": 25, "Posición": "Base", "Número de Camiseta": 2, "Equipo": 'Bucos de Santander', "Puntos": 100, "Rebotes": 40, "Asistencias": 60, "Robos": 18},
                       { "ID": 7, "Nombre": "Alberto Ruiz", "Edad": 30, "Posición": "Escolta", "Número de Camiseta": 6, "Equipo": 'Bucos de Santander', "Puntos": 115, "Rebotes": 55, "Asistencias": 45, "Robos": 22},
                       { "ID": 8, "Nombre": "Francisco Jiménez", "Edad": 23, "Posición": "Alero", "Número de Camiseta": 9, "Equipo": 'Bucos de Santander', "Puntos": 125, "Rebotes": 65, "Asistencias": 35, "Robos": 28},
                       { "ID": 9, "Nombre": "Jorge Ramírez", "Edad": 27, "Posición": "Pívot", "Número de Camiseta": 14, "Equipo": 'Bucos de Santander', "Puntos": 135, "Rebotes": 85, "Asistencias": 25, "Robos": 12},
                       { "ID": 10, "Nombre": "Andrés Castillo", "Edad": 24, "Posición": "Ala-pívot", "Número de Camiseta": 4, "Equipo": 'Bucos de Santander', "Puntos": 105, "Rebotes": 75, "Asistencias": 15, "Robos": 14},
                       { "ID": 11, "Nombre": "Ricardo Mendoza", "Edad": 29, "Posición": "Base", "Número de Camiseta": 1, "Equipo": 'Bucos de Santander', "Puntos": 95, "Rebotes": 35, "Asistencias": 55, "Robos": 16},
                       { "ID": 12, "Nombre": "Héctor Vargas", "Edad": 26, "Posición": "Escolta", "Número de Camiseta": 8, "Equipo": 'Bucos de Santander', "Puntos": 112, "Rebotes": 52, "Asistencias": 42, "Robos": 24},
                       { "ID": 13, "Nombre": "Mario Hernández", "Edad": 28, "Posición": "Alero", "Número de Camiseta": 10, "Equipo": 'Gigantes de Occidente', "Puntos": 128, "Rebotes": 68, "Asistencias": 38, "Robos": 26},
                       { "ID": 14, "Nombre": "Pablo Sánchez", "Edad": 25, "Posición": "Pívot", "Número de Camiseta": 12, "Equipo": 'Gigantes de Occidente', "Puntos": 138, "Rebotes": 88, "Asistencias": 28, "Robos": 13},
                       { "ID": 15, "Nombre": "Santiago López", "Edad": 30, "Posición": "Ala-pívot", "Número de Camiseta": 13, "Equipo": 'Gigantes de Occidente', "Puntos": 108, "Rebotes": 78, "Asistencias": 18, "Robos": 11},
                       { "ID": 16, "Nombre": "Fernando García", "Edad": 23, "Posición": "Base", "Número de Camiseta": 2, "Equipo": 'Gigantes de Occidente', "Puntos": 98, "Rebotes": 38, "Asistencias": 58, "Robos": 17},
                       { "ID": 17, "Nombre": "Javier Rodríguez", "Edad": 27, "Posición": "Escolta", "Número de Camiseta": 5, "Equipo": 'Gigantes de Occidente', "Puntos": 118, "Rebotes": 58, "Asistencias": 48, "Robos": 23},
                       { "ID": 18, "Nombre": "Andrés Ramírez", "Edad": 24, "Posición": "Alero", "Número de Camiseta": 11, "Equipo": 'Gigantes de Occidente', "Puntos": 122, "Rebotes": 62, "Asistencias": 32, "Robos": 27},
                       { "ID": 19, "Nombre": "Diego Fernández", "Edad": 29, "Posición": "Pívot", "Número de Camiseta": 14, "Equipo": 'Gigantes de Occidente', "Puntos": 132, "Rebotes": 82, "Asistencias": 22, "Robos": 14},
                       { "ID": 20, "Nombre": "Luis Gómez", "Edad": 26, "Posición": "Ala-pívot", "Número de Camiseta": 4, "Equipo": 'Gigantes de Occidente', "Puntos": 102, "Rebotes": 72, "Asistencias": 12, "Robos": 10},
                       { "ID": 21, "Nombre": "Carlos Torres", "Edad": 28, "Posición": "Base", "Número de Camiseta": 1, "Equipo": 'Gigantes de Occidente', "Puntos": 92, "Rebotes": 32, "Asistencias": 52, "Robos": 15},
                       { "ID": 22, "Nombre": "Jorge Jiménez", "Edad": 25, "Posición": "Escolta", "Número de Camiseta": 6, "Equipo": 'Gigantes de Occidente', "Puntos": 110, "Rebotes": 54, "Asistencias": 44, "Robos": 21},
                       { "ID": 23, "Nombre": "Miguel Castillo", "Edad": 30, "Posición": "Alero", "Número de Camiseta": 9, "Equipo": 'Gigantes de Occidente', "Puntos": 124, "Rebotes": 66, "Asistencias": 36, "Robos": 29},
                       { "ID": 24, "Nombre": "Ricardo Hernández", "Edad": 23, "Posición": "Pívot", "Número de Camiseta": 15, "Equipo": 'Gigantes de Occidente',"Puntos": 134, "Rebotes": 86, "Asistencias": 26, "Robos": 12},]

#VOLEIBOL: Incluye puntos anotados, bloqueos, aces (saques ganadores), recepciones efectivas
jugadores_voleibol = [
    { "ID": 1, "Nombre": "Andrés Torres", "Edad": 24, "Posición": "Posiciones del cuerpo", "Número de Camiseta": 8, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 200, "Bloqueos": 50, "Servicios Aces": 30, "Recepciones Efectivas": 80, "Aces": 30, "Recepciones": 80},
    { "ID": 2, "Nombre": "Jorge Díaz", "Edad": 28, "Posición": "Atacante", "Número de Camiseta": 4, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 180, "Bloqueos": 70, "Servicios Aces": 20, "Recepciones Efectivas": 90, "Aces": 20, "Recepciones": 90},
    { "ID": 3, "Nombre": "Raúl Morales", "Edad": 26, "Posición": "Zaguero", "Número de Camiseta": 2, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 150, "Bloqueos": 30, "Servicios Aces": 10, "Recepciones Efectivas": 100, "Aces": 10, "Recepciones": 100},
    { "ID": 4, "Nombre": "Iván Jiménez", "Edad": 29, "Posición": "Rematador medio", "Número de Camiseta": 10, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 190, "Bloqueos": 60, "Servicios Aces": 25, "Recepciones Efectivas": 85, "Aces": 25, "Recepciones": 85},
    { "ID": 5, "Nombre": "Oscar Ruiz", "Edad": 25, "Posición": "Colocador", "Número de Camiseta": 1, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 160, "Bloqueos": 40, "Servicios Aces": 15, "Recepciones Efectivas": 95, "Aces": 15, "Recepciones": 95},
    { "ID": 6, "Nombre": "Pablo Castillo", "Edad": 27, "Posición": "Bloqueador", "Número de Camiseta": 14, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 170, "Bloqueos": 65, "Servicios Aces": 18, "Recepciones Efectivas": 88, "Aces": 18, "Recepciones": 88},
    { "ID": 7, "Nombre": "Santiago Flores", "Edad": 30, "Posición": "Rematador opuesto", "Número de Camiseta": 9, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 210, "Bloqueos": 55, "Servicios Aces": 28, "Recepciones Efectivas": 82, "Aces": 28, "Recepciones": 82},
    { "ID": 8, "Nombre": "Alberto Vega", "Edad": 23, "Posición": "Colocador", "Número de Camiseta": 7, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 175, "Bloqueos": 45, "Servicios Aces": 22, "Recepciones Efectivas": 89, "Aces": 22, "Recepciones": 89},
    { "ID": 9, "Nombre": "Ricardo Herrera", "Edad": 28, "Posición": "Atacantes", "Número de Camiseta": 5, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 155, "Bloqueos": 35, "Servicios Aces": 12, "Recepciones Efectivas": 98, "Aces": 12, "Recepciones": 98},
    { "ID": 10, "Nombre": "Daniel Silva", "Edad": 26, "Posición": "Atacantes", "Número de Camiseta": 3, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 165, "Bloqueos": 42, "Servicios Aces": 17, "Recepciones Efectivas": 92, "Aces": 17, "Recepciones": 92},
    { "ID": 11, "Nombre": "Francisco Gómez", "Edad": 29, "Posición": "Bloqueadores", "Número de Camiseta": 13, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 185, "Bloqueos": 68, "Servicios Aces": 21, "Recepciones Efectivas": 87, "Aces": 21, "Recepciones": 87},
    { "ID": 12, "Nombre": "Javier Torres", "Edad": 25, "Posición": "Rematador opuesto", "Número de Camiseta": 6, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 195, "Bloqueos": 52, "Servicios Aces": 27, "Recepciones Efectivas": 83, "Aces": 27, "Recepciones": 83},
    { "ID": 13, "Nombre": "Miguel Ramírez", "Edad": 27, "Posición": "Atacante", "Número de Camiseta": 15, "Equipo": 'Virtus Guanajuato', "Puntos Anotados": 178, "Bloqueos": 48, "Servicios Aces": 23, "Recepciones Efectivas": 90, "Aces": 23, "Recepciones": 90},
    { "ID": 14, "Nombre": "Luis Fernández", "Edad": 24, "Posición": "Colocador", "Número de Camiseta": 11, "Equipo": 'Voley Xalapa', "Puntos Anotados": 158, "Bloqueos": 33, "Servicios Aces": 14, "Recepciones Efectivas": 97, "Aces": 14, "Recepciones": 97},
    { "ID": 15, "Nombre": "Carlos Sánchez", "Edad": 28, "Posición": "Rematador opuesto", "Número de Camiseta": 1, "Equipo": 'Voley Xalapa', "Puntos Anotados": 168, "Bloqueos": 41, "Servicios Aces": 16, "Recepciones Efectivas": 93, "Aces": 16, "Recepciones": 93},
    { "ID": 16, "Nombre": "Diego López", "Edad": 26, "Posición": "Zaguero", "Número de Camiseta": 4, "Equipo": 'Voley Xalapa', "Puntos Anotados": 188, "Bloqueos": 66, "Servicios Aces": 19, "Recepciones Efectivas": 86, "Aces": 19, "Recepciones": 86},
    { "ID": 17, "Nombre": "Javier Martínez", "Edad": 29, "Posición": "Zaguero", "Número de Camiseta": 9, "Equipo": 'Voley Xalapa', "Puntos Anotados": 198, "Bloqueos": 54, "Servicios Aces": 29, "Recepciones Efectivas": 81, "Aces": 29, "Recepciones": 81},
    { "ID": 18, "Nombre": "Sergio Rodríguez", "Edad": 25, "Posición": "Atacantes", "Número de Camiseta": 7, "Equipo": 'Voley Xalapa', "Puntos Anotados": 178, "Bloqueos": 46, "Servicios Aces": 24, "Recepciones Efectivas": 88, "Aces": 24, "Recepciones": 88},
    { "ID": 19, "Nombre": "Andrés Gómez", "Edad": 27, "Posición": "Bloquedor", "Número de Camiseta": 2, "Equipo": 'Voley Xalapa', "Puntos Anotados": 162, "Bloqueos": 36, "Servicios Aces": 13, "Recepciones Efectivas": 99, "Aces": 13, "Recepciones": 99},
    { "ID": 20, "Nombre": "Pablo Hernández", "Edad": 30, "Posición": "Rematador medio", "Número de Camiseta": 3, "Equipo": 'Voley Xalapa', "Puntos Anotados": 172, "Bloqueos": 43, "Servicios Aces": 15, "Recepciones Efectivas": 94, "Aces": 15, "Recepciones": 94},
    { "ID": 21, "Nombre": "Fernando Jiménez", "Edad": 23, "Posición": "Colocador", "Número de Camiseta": 12, "Equipo": 'Voley Xalapa', "Puntos Anotados": 182, "Bloqueos": 64, "Servicios Aces": 20, "Recepciones Efectivas": 85, "Aces": 20, "Recepciones": 85},
    { "ID": 22, "Nombre": "Ricardo Martínez", "Edad": 28, "Posición": "Zagueros", "Número de Camiseta": 10, "Equipo": 'Voley Xalapa', "Puntos Anotados": 202, "Bloqueos": 56, "Servicios Aces": 31, "Recepciones Efectivas": 80, "Aces": 31, "Recepciones": 80},
    { "ID": 23, "Nombre": "Jorge Castillo", "Edad": 26, "Posición": "Atacantes", "Número de Camiseta": 6, "Equipo": 'Voley Xalapa', "Puntos Anotados": 180, "Bloqueos": 49, "Servicios Aces": 22, "Recepciones Efectivas": 89, "Aces": 22, "Recepciones": 89},
    { "ID": 24, "Nombre": "Miguel Ramírez", "Edad": 29, "Posición": "Colocador", "Número de Camiseta": 5, "Equipo": 'Voley Xalapa', "Puntos Anotados": 160, "Bloqueos": 34, "Servicios Aces": 11, "Recepciones Efectivas": 98, "Aces": 11, "Recepciones": 98},
]
            
#Número mínimo y máximo de jugadores por deporte.
limite = {1: (11, 18),  # Fútbol: 11-18 jugadores
          2: (5, 12),  # Baloncesto: 5-12 jugadores
          3: (6, 14)   # Voleibol: 6-14 jugadores
         }
equipos = [
    {"Nombre": "Atlético Nacional", "Deporte": 1, "Jugadores": [12]},
    {"Nombre": "Deportivo Cali", "Deporte": 1, "Jugadores": [14]},
    {"Nombre": "Millonarios", "Deporte": 1, "Jugadores": [13]},
    {"Nombre": "Bucos de Santander", "Deporte": 2, "Jugadores": [11]},
    {"Nombre": "Gigantes de Occidente", "Deporte": 2, "Jugadores": [12]},
    {"Nombre": "Virtus Guanajuato", "Deporte": 3, "Jugadores": [13]},
    {"Nombre": "Voley Xalapa", "Deporte": 3, "Jugadores": [9]}
]
deportes = [1, 2, 3]  # 1: Fútbol, 2: Baloncesto, 3: Voleibol
canchas = [[1, "Cancha Central"], [2, "Cancha Norte"], [3, "Cancha Sur"], [4, "Cancha Este"], [5, "Cancha Oeste"]]

while True:
    menu()
    opcion = (input("Seleccione una opción: "))

#Aquí vamos con la opción de registrar equipos

    if opcion == "1":
        nombre_equipo = input("Ingrese el nombre del equipo: ")
        deporte = int(input("Seleccione el deporte (1: Fútbol, 2: Baloncesto, 3: Voleibol): "))

        if deporte in deportes:
            equipos.append({"Nombre": nombre_equipo, "Deporte": deporte, "Jugadores": []})

            if nombre_equipo not in tabla_posiciones:
                tabla_posiciones[nombre_equipo] = {
                    "Deporte": deporte,
                    "Puntos":0,
                    "Partidos Jugados":0,
                    "Ganados":0,
                    "Empatados":0,
                    "Perdidos":0,
                    "Puntos a Favor":0,
                    "Puntos en Contra":0,
                    "Diferencia":0
                }

            print(f"Equipo '{nombre_equipo}' registrado para el deporte deseado.")
        else:
            print("Deporte no válido.")

    # Submenu para gestionar equipos y jugadores de un deporte específico
    # Permite agregar/eliminar jugadores y ver información de equipos

    elif opcion == "2":
        print("\n---Gestión de múltiples deportes seleccionada.--")
        print("\n---Elija una opción:---")
        print("1. Fútbol")
        print("2. Baloncesto")
        print("3. Voleibol")
        deporte_seleccionado = int(input("Seleccione el deporte (1-3): "))
       
#Al ser básicamente un submenú, realizaremos más abajo una variable llamada sub_opción para manejar las opciones internas.
#Empezando con fútbol

        if deporte_seleccionado == 1:
            # GESTIÓN DE FÚTBOL - Submenu para equipos y jugadores de fútbol
            print("Gestión de equipos de Fútbol")
            print("1. Agregar jugador")
            print("2. Eliminar jugador")
            print("3. Ver lista de jugadores")
            print("4. Ver todos los equipos de fútbol.")
            print("5. Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":
                agregar_jugador_generic(1)
            elif sub_opcion == "2":
                eliminar_jugador_generic(1)
            elif sub_opcion == "3":
                listar_jugadores_deporte(1)
            elif sub_opcion == "4":
                print("Equipos de Fútbol registrados:")
                encontrados = False
                for eq in equipos:
                    if eq["Deporte"] == 1:
                        print(eq)
                        encontrados = True
                if not encontrados:
                    print("No hay equipos de fútbol registrados.")
            elif sub_opcion == "5":
                continue

#Ahora seguimos con la gestión de equipos de baloncesto.

        elif deporte_seleccionado == 2:
            # GESTIÓN DE BALONCESTO - Submenu para equipos y jugadores de baloncesto
            print("Gestión de equipos de Baloncesto")
            print("1. Agregar jugador")
            print("2. Eliminar jugador")
            print("3. Ver lista de jugadores")
            print("4. Ver todos los equipos de baloncesto.")
            print("5. Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":
                agregar_jugador_generic(2)
            elif sub_opcion == "2":
                eliminar_jugador_generic(2)
            elif sub_opcion == "3":
                listar_jugadores_deporte(2)
            elif sub_opcion == "4":
                print("Equipos de Baloncesto registrados:")
                encontrados = False
                for eq in equipos:
                    if eq["Deporte"] == 2:
                        print(eq)
                        encontrados = True
                if not encontrados:
                    print("No hay equipos de baloncesto registrados.")
            elif sub_opcion == "5":
                continue

#Ahora seguimos con la gestión de equipos de voleibol.

        elif deporte_seleccionado == 3:
            # GESTIÓN DE VOLEIBOL - Submenu para equipos y jugadores de voleibol
            print("Gestión de equipos de Voleibol")
            print("1. Agregar jugador")
            print("2. Eliminar jugador")
            print("3. Ver lista de jugadores")
            print("4. Ver todos los equipos de voleibol.")
            print("5. Volver al menú principal")
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == "1":
                agregar_jugador_generic(3)
            elif sub_opcion == "2":
                eliminar_jugador_generic(3)
            elif sub_opcion == "3":
                listar_jugadores_deporte(3)
            elif sub_opcion == "4":
                print("Equipos de Voleibol registrados:")
                encontrados = False
                for eq in equipos:
                    if eq["Deporte"] == 3:
                        print(eq)
                        encontrados = True
                if not encontrados:
                    print("No hay equipos de voleibol registrados.")
            elif sub_opcion == "5":
                continue

    elif opcion == "3":
# Verifica que cada equipo cumpla con el número mínimo y máximo de jugadores
        print("Validación de cupos por deporte seleccionada.")
        for eq in equipos:
            deporte = eq["Deporte"]
            # Aquí contaremos a todos los jugadores del equipo según el deporte y equipo.
            if deporte == 1:
                num_jugadores = sum(1 for j in jugadores_futbol if j.get("Equipo") == eq["Nombre"])
            elif deporte == 2:
                num_jugadores = sum(1 for j in jugadores_baloncesto if j.get("Equipo") == eq["Nombre"])
            elif deporte == 3:
                num_jugadores = sum(1 for j in jugadores_voleibol if j.get("Equipo") == eq["Nombre"])
            else:
                num_jugadores = len(eq.get("Jugadores", []))
            min_jugadores, max_jugadores = limite[deporte]
            if num_jugadores < min_jugadores:
                print(f"El equipo '{eq['Nombre']}' tiene menos jugadores ({num_jugadores}) que el mínimo requerido ({min_jugadores}) para su deporte.")
            elif min_jugadores < num_jugadores < max_jugadores:
                print(f"El equipo '{eq['Nombre']}' tiene {num_jugadores} jugadores: cumple con el número mínimo requerido ({min_jugadores}) y está dentro del rango permitido ({min_jugadores}-{max_jugadores}).")
            elif num_jugadores > max_jugadores:
                print(f"El equipo '{eq['Nombre']}' tiene más jugadores ({num_jugadores}) que el máximo permitido ({max_jugadores}) para su deporte.")
            else:
                #Estos casos serán límite, pero se pueden dar.
                if num_jugadores == min_jugadores:
                    print(f"El equipo '{eq['Nombre']}' tiene exactamente el número mínimo requerido ({min_jugadores}).")
                else:
                    print(f"El equipo '{eq['Nombre']}' tiene exactamente el número máximo permitido ({max_jugadores}).")

    elif opcion == "4":
# Crea el calendario automático de todos los partidos del torneo.
# Sistema: Todos contra todos (round-robin) con distribución de fechas, horarios y canchas
        print("\n---Generación de Fixture seleccionada.--")
        fecha_inicio_input = input("Ingrese la fecha de inicio del torneo (Día-Mes-Año) o presione Enter para usar mañana: ")
        try:
            if fecha_inicio_input.strip():
                fecha_inicio = datetime.strptime(fecha_inicio_input, "%d-%m-%Y")
            else:
                fecha_inicio = datetime.now() + timedelta(days=1)
        except ValueError:
            print("Formato de fecha inválido. Usando mañana como fecha de inicio.")
            fecha_inicio = datetime.now() + timedelta(days=1)

        fixture = generar_full_fixture(fecha_inicio, dias_entre_rondas=2, horarios=["10:00AM", "3:00PM", "7:00PM"])
        if not fixture:
            print("No se generó ningún partido (quizá no hay equipos suficientes en algún deporte).")
        else:
            # Guardar fixture generado en la lista global de partidos pendientes
            partidos_pendientes = fixture
            print("\nFixture generado y guardado en 'partidos_pendientes' (Round-Robin - todos contra todos):")
            for partido in partidos_pendientes:
                print(partido)
            print(f"\nTotal partidos: {len(partidos_pendientes)}. Ahora puede registrar resultados desde la opción 5.")

    elif opcion == "5":
# Permite ingresar los resultados de partidos pendientes y actualizar tabla de posiciones
        registrar_resultado_partido()

    elif opcion == "6":
    # Sumar estadísticas de jugadores después de un partido (goles, puntos, aces, etc.)
        try:
            deporte_reg = int(input("Seleccione el deporte para registrar estadísticas (1: Fútbol, 2: Baloncesto, 3: Voleibol): "))
            if deporte_reg in (1,2,3):
                registrar_estadisticas_jugador(deporte_reg)
            else:
                print("Deporte no válido.")
        except ValueError:
            print("Entrada inválida.")

    elif opcion == "7":
    # Muestra rankings de mejores jugadores por estadística en cada deporte
        # Mostrar ranking de jugadores
        mostrar_ranking_jugadores(None)

    elif opcion == "8":
    # Muestra tabla ordenada de posiciones para el deporte seleccionado
        mostrar_tabla_posiciones()
    
    elif opcion == "9":
    # Accede a menú de reportes analíticos: fixture, top ofensivo/defensivo, historial, predicción.
        print("\n---Mostrando reportes de torneos.---")
        mostrar_reportes_torneo()

    elif opcion == "0":
        print("Saliendo del programa. ¡Hasta luego!")
        break