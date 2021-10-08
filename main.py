import random
import sys

random.seed(10)

def obtener_dist_maxima():
    return float(input("Ingrese la distancia maxima: "))


def obtener_archivo_salida():
    valor_defecto = "jugadas.txt"
    nombre_archivo = input("Ingrese un nombre para el archivo de salida: (por defecto es " + valor_defecto + ")")
    if nombre_archivo == "":
        nombre_archivo = valor_defecto
    return nombre_archivo


def crear_jugador(line):
    nombre, edad, localidad = line.split(',')
    localidad = localidad[:-1]
    edad = int(edad)
    return (nombre, edad, localidad)


def crear_dist_localidades(line):
    localidad1, localidad2, distancia = line.split(',')
    localidad2 = localidad2[1:]
    distancia = float(distancia[1:])
    return (localidad1, localidad2, distancia)


def separar_edades(jugadores):
    menores = list(filter(lambda jugador: (jugador[1] <= 17), jugadores))
    mayores = list(filter(lambda jugador: (jugador[1] > 17), jugadores))
    return menores, mayores


def generar_elementos_archivo(archivo, funcion_generadora):
    """
    generar_elementos_archivo : string (string -> X) -> List(X)
    generar_elementos_archivo toma un string que representa
    el nombre de un archivo a leer, y una funcion funcion_generadora.
    Se recorren todas las lineas del archivo, y estas son pasadas a funcion_generadora
    como argumento. El valor de retorno de esta ultima es agregada a una lista la cual
    sera el valor de retorno de generar_elementos_archivo.
    """
    elementos_generados = []
    with open(archivo, 'r') as f:
        for linea in f.readlines():
            elemento = funcion_generadora(linea)
            elementos_generados.append(elemento)
    return elementos_generados


def duelo(jugador1, jugador2):
    peleadores = [jugador1, jugador2]
    random.shuffle(peleadores)
    return peleadores


def obtener_dist_localidades(distancias, localidad1, localidad2):
    if localidad1 == localidad2:
        return 0.0
    else:
        par_localidades = set((localidad1, localidad2))
        for tupla_ciudad_distancia in distancias:
            if par_localidades == {tupla_ciudad_distancia[0], tupla_ciudad_distancia[1]}:
                return tupla_ciudad_distancia[2]


def distancia_valida(n, distancias, ciudad1, ciudad2):
    dist = obtener_dist_localidades(distancias, ciudad1, ciudad2)
    return dist < n


def obtener_set_ciudades(distancias):
    ciudades = set()
    for item in distancias:
        ciudades.add(item[0])
        ciudades.add(item[1])
    return ciudades


def jugada_en_misma_ciudad(lista_ciudades, jugadores, archivo_output):
    ganadores_regionales = []
    for ciudad in lista_ciudades:
        ganador_regional = jugar(ciudad, jugadores, archivo_output)
        ganadores_regionales.append(ganador_regional)

    return ganadores_regionales


def jugar(ciudad, jugadores, archivo_output):
    jugadores_ciudad = list(filter(lambda jugador: (jugador[2] == ciudad), jugadores))
    if len(jugadores_ciudad) == 1:
        ganador = jugadores_ciudad[0]
    elif len(jugadores_ciudad) == 0:
        return tuple()
    with open(archivo_output, "a") as f:
        while len(jugadores_ciudad) > 1:
            jugador1 = random.choice(jugadores_ciudad)
            jugadores_ciudad.remove(jugador1)
            jugador2 = random.choice(jugadores_ciudad)
            jugadores_ciudad.remove(jugador2)
            ganador, perdedor = duelo(jugador1,jugador2)
            jugadores_ciudad.append(ganador)
            linea = ganador[0] + " eliminó a " + perdedor[0] + "\n"
            f.write(linea)
    return ganador


def jugada_por_regiones(ciudades, ganadores_regionales, radio_maximo, local_dist, archivo_output):
    ganadores_locales = []
    peleadores_potenciales = []
    random.shuffle(ganadores_regionales)
    with open(archivo_output, "a") as f:
        for ganador_r in ganadores_regionales:
            ciudades_cercanas = list(filter(lambda ciudad: distancia_valida(radio_maximo, local_dist, ganador_r[2], ciudad), ciudades))
            if ciudades_cercanas == []:
                ganadores_locales.append(ganador_r)
            for item in ganadores_regionales:
                if item[2] in ciudades_cercanas:
                    peleadores_potenciales.append(item)
            jugador2 = random.choice(peleadores_potenciales)
            ganador_final, perdedor = duelo(ganador_r,jugador2)
            linea = ganador_final[0] + " eliminó a " + perdedor[0] + "\n"
            f.write(linea)
    if ganadores_locales == []:
        anunciar_ganador(ganador_final, archivo_output)
    else:
        anunciar_varios_ganadores(ganadores_locales, archivo_output)


def anunciar_ganador(ganador, archivo_output):
    with open(archivo_output, 'a') as f:
        anuncio_ganador = ganador[0] + " es el ganador."
        f.write(anuncio_ganador)


def anunciar_varios_ganadores(ganadores_locales, archivo_output):
    anuncio_ganadores = "Los ganadores son: "
    for ganador_local in ganadores_locales:
        anuncio_ganadores += ganador_local[0] + ", " 
    with open(archivo_output, 'a') as f:
        f.write(anuncio_ganadores)
        f.write("\n" * 3)


def anunciar_ganador(ganador, archivo_output):
    with open(archivo_output, 'a') as f:
        anuncio_ganador = ganador[0] + " es el ganador."
        f.write(anuncio_ganador)
        f.write("\n" * 3)


def limpiar(archivo_output):
    with open(archivo_output, 'w') as f:
        f.write("")


def main():
    # Se obtiene desde la terminal el nombre de los 
    # archivos de jugadores y distancias
    archivo_jugadores, archivo_distancias = sys.argv[1:]
    
    # Pedimos como input el nombre del archivo de salida
    #archivo_output = obtener_archivo_salida()
    archivo_output = "jugadas.txt"
    # Obtenemos N, la distancia máxima a realizar los enfrentamientos
    #N = obtener_dist_maxima()
    N = 100
    # Definimos la lista de tuplas de la forma (nombre, edad, localidad)
    jugadores = generar_elementos_archivo(archivo_jugadores, crear_jugador)

    # Reducimos la cantidad de jugadores para realizar pruebas
    jugadores = jugadores[:200]

    # Separamos la lista de jugadores entre los que son menores y mayores de edad
    jugadores_menores, jugadores_mayores = separar_edades(jugadores)
    
    # Obtenemos la lista de tuplas de la forma (ciudad, ciudad, distancia)
    distancias_localidades = generar_elementos_archivo(archivo_distancias, crear_dist_localidades)

    # Definimos un set con todos los nombres de las distintas ciudades
    ciudades = obtener_set_ciudades(distancias_localidades)

    # Limpiamos el archivo que se usará de output
    limpiar(archivo_output)

    # Realizamos la instancia de enfrentamientos de mayores de edad, primero por ciudades
    # y luego, entre los ganadores se enfrentarán por regiones/ciudades, solo si se
    # encuentran en el radio permitido
    ganadores_regionales_mayores = jugada_en_misma_ciudad(ciudades,jugadores_mayores, archivo_output)
    jugada_por_regiones(ciudades, ganadores_regionales_mayores, N,distancias_localidades,archivo_output)
    

    # Realizamos la instancia de enfrentamientos de menores de edad, primero por ciudades
    # y luego, entre los ganadores se enfrentarán por regiones/ciudades, solo si se
    # encuentran en el radio permitido
    ganadores_regionales_menores = jugada_en_misma_ciudad(ciudades,jugadores_menores, archivo_output)
    jugada_por_regiones(ciudades, ganadores_regionales_menores, N, distancias_localidades,archivo_output)

    print("El archivo " + archivo_output + " fue escrito.")

if __name__ == "__main__":
    main()
