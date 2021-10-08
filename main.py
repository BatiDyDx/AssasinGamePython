import random
import sys

random.seed(10)

def obtener_dist_maxima():
    """
    obtener_dist_maxima : None -> Float
    obtener_dist_maxima pide al usuario introducir un numero,
    que se usará como distancia maxima para realizar las batallas
    entre ciudades
    """
    return float(input("Ingrese la distancia maxima: "))


def obtener_archivo_salida():
    """
    obtener_archivo_salida : None -> String
    obtener_archivo_salida pide al usuario introducir
    un nombre al archivo que se usará para escribir el output
    del programa. Si no se introduce nada, el valor por defecto
    será jugadas.txt
    """
    valor_defecto = "jugadas.txt"
    nombre_archivo = input("Ingrese un nombre para el archivo de salida: (por defecto es " + valor_defecto + ")")
    # Si el usuario no introduce ningun valor, retornamos el valor por defecto
    if nombre_archivo == "":
        nombre_archivo = valor_defecto
    return nombre_archivo


def crear_jugador(line):
    """
    crear_jugador : String -> Tuple(String, Int, String)
    crear_jugador toma una linea de texto, con formato
    nombre,edad,localidad; y devuelve una tupla de la forma
    (nombre, edad, localidad)
    """
    nombre, edad, localidad = line.split(',')
    # Quitamos el caracter \n de localidad
    localidad = localidad[:-1]
    # Convertimos la edad a un int
    edad = int(edad)
    return (nombre, edad, localidad)


def crear_dist_localidades(line):
    """
    crear_dist_localidades : String -> Tuple(String, String, Float)
    crear_dist_localidades toma una linea de texto, con formato
    localidad1, localidad2, distancia_entre_localidades, y devuelve
    una tupla de la forma (localidad1, localidad2, distancia_entre_localidades)
    """
    localidad1, localidad2, distancia = line.split(',')
    # Dado el formato de distancias.txt, debemos quitar el primer
    # caracter de localidad2, ya que es un espacio en blanco
    localidad2 = localidad2[1:]
    # Convertimos la distancia a float
    distancia = float(distancia)
    return (localidad1, localidad2, distancia)


def separar_edades(jugadores):
    """
    separar_edades : List(Tuple(String, Int, String)) -> Tuple(List(Tuple(String, Int, String)))
    separar_edades toma una lista de jugadores de la forma (nombre, edad, localidad),
    y devuelve una tupla de dos listas, la primera siendo de jugadores menores de edad, y la segunda
    de jugadores mayores de edad.
    """
    edad_minima_adulto = 18
    menores = list(filter(lambda jugador: (jugador[1] < edad_minima_adulto ), jugadores))
    mayores = list(filter(lambda jugador: (jugador[1] >= edad_minima_adulto), jugadores))
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
    """
    duelo : Tuple(String, Int, String) Tuple(String, Int, String) -> List(Tuple(String, Int, String) Tuple(String, Int, String))
    duelo recibe dos jugadores, y devuelve una lista con los dos elementos en orden
    aleatorio. El primer elemento de la lista será interpretado como el ganador, y
    el segundo como el perdedor
    """
    peleadores = [jugador1, jugador2]
    random.shuffle(peleadores)
    return peleadores


def obtener_dist_localidades(distancias, localidad1, localidad2):
    """
    obtener_dist_localidades : List(Tuple(String, String, Float)) String String -> Float
    obtener_dist_localidades recibe una lista de tuplas (que representan distancias entre
    pares de ciudades), y dos ciudades, y retorna la distancia entre estas 
    """
    if localidad1 == localidad2:
        return 0.0
    else:
        par_localidades = set((localidad1, localidad2))
        for tupla_ciudad_distancia in distancias:
            if par_localidades == {tupla_ciudad_distancia[0], tupla_ciudad_distancia[1]}:
                return tupla_ciudad_distancia[2]


def distancia_valida(n, distancias, ciudad1, ciudad2):
    """
    distancia_valida : Float List(Tuple(String, String, Float)) String String -> Bool
    distancia_valida determina si dos ciudades estan a una distancia válida dado un número n
    """
    dist = obtener_dist_localidades(distancias, ciudad1, ciudad2)
    return dist < n


def obtener_set_ciudades(distancias):
    """
    obtener_set_ciudades : List(Tuple(String, String, Float)) -> Set(String)
    obtener_set_ciudades recibe una lista de tuplas (que representan distancias entre
    pares de ciudades), y retorna un set con los nombres de todas las ciudades que entran
    en el juego.
    """
    ciudades = set()
    for item in distancias:
        ciudades.add(item[0])
        ciudades.add(item[1])
    return ciudades


def jugada_en_misma_ciudad(lista_ciudades, jugadores, archivo_output):
    # ciudad_jugadores es un diccionario donde la llave es un string con el nombre
    # de una ciudad, y el valor es una lista de tuplas (que represenentan jugadores)
    # de los jugadores de dicha ciudad
    ciudad_jugadores = dict() 
    for ciudad in lista_ciudades:
        ciudad_jugadores[ciudad] = list(filter(lambda jugador:(jugador[2] == ciudad), jugadores))
    ganadores_regionales = jugar(jugadores, ciudad_jugadores, lista_ciudades, archivo_output)
    return ganadores_regionales


def jugar(jugadores, ciudad_jugadores, lista_ciudades, archivo_output):
    ganadores_regionales = []
    copia_jugadores = jugadores[:]
    with open(archivo_output, "a") as f:
        # Mientras la cantidad de jugadores sea distinta de la cantidad de
        # localidades, significa que todavia no hay un ganador por cada localidad
        while len(copia_jugadores) > len(lista_ciudades):
            jugador = random.choice(copia_jugadores)
            jugadores_en_ciudad = ciudad_jugadores[jugador[2]]
            if len(jugadores_en_ciudad) > 1:
                jugadores_en_ciudad.remove(jugador)
                jugador2 = random.choice(jugadores_en_ciudad)
                jugadores_en_ciudad.remove(jugador2)
                ganador, perdedor = duelo(jugador,jugador2)
                jugadores_en_ciudad.append(ganador)
                copia_jugadores.remove(jugador2)
                linea = ganador[0] + " eliminó a " + perdedor[0] + "\n"
                f.write(linea)
            elif len(jugadores_en_ciudad) == 1:
                # Si queda solo un jugador en la ciudad, el ganador será este 
                ganadores_regionales.append(jugadores_en_ciudad[0])
    return ganadores_regionales


def jugada_por_regiones(lista_ciudades, ganadores_regionales, n,local_dist, archivo_output):
    ganadores_locales = []
    peleadores_potenciales = []
    ganador_final = []
    ciudades_cercanas = []
    ganadores_copia = ganadores_regionales[:]
    random.shuffle(ganadores_regionales)
    with open(archivo_output, "a") as f:
        for ganador_r in ganadores_regionales:
            ciudades_cercanas = list(filter(lambda ciudad: distancia_valida(n, local_dist, ganador_r[2], ciudad), lista_ciudades))
            for item in ganadores_copia:
                if item[2] in ciudades_cercanas and not item == ganador_r:
                    peleadores_potenciales.append(item)
            if ciudades_cercanas == [] or peleadores_potenciales == []:
                ganadores_locales.append(ganador_r)
            elif ganador_r in ganadores_copia:
                jugador2 = random.choice(peleadores_potenciales)
                ganador_final = duelo(ganador_r,jugador2)
                perdedor = ganador_r if jugador2 == ganador_final else jugador2
                ganadores_copia.remove(perdedor)
                linea = ganador_final[0] + " eliminó a " + perdedor[0] + "\n"
                f.write(linea)
                peleadores_potenciales = []
    if ganadores_locales == []:
        anunciar_ganador(ganador_final, archivo_output)
    else:
        anunciar_varios_ganadores(ganadores_locales, archivo_output)


def anunciar_ganador(ganador, archivo_output):
    """
    anunciar_ganador : Tuple(String, Int, String) String -> None
    Recibe una tupla que representa al jugador ganador, y el nombre
    del archivo a escribir al output, y escribe en el archivo una
    linea anunciando el nombre del ganador
    """
    with open(archivo_output, 'a') as f:
        anuncio_ganador = ganador[0] + " es el ganador."
        f.write(anuncio_ganador)
        f.write("\n" * 3)


def anunciar_varios_ganadores(ganadores_locales, archivo_output):
    """
    anunciar_ganador : List(Tuple(String, Int, String)) String -> None
    Recibe una tupla que representa a los ganadores regionales, y el nombre
    del archivo a escribir al output, y escribe en el archivo una
    linea anunciando los nombres de los ganadores.
    """
    anunciar_ganadores = "Los ganadores son: "
    # Agrega el nombre de los ganadores a la linea a escribir
    for ganador_local in ganadores_locales:
        anunciar_ganadores += ganador_local[0] + ", " 
    with open(archivo_output, 'a') as f:
        f.write(anunciar_ganadores)
        f.write("\n" * 3)


def iniciar_juego(categoria, archivo_output):
    """
    iniciar_partida : String String -> None
    Toma una categoria de jugadores y el nombre del archivo a escribir
    el output, y escribe la categoria a que va a jugar
    """
    with open(archivo_output, 'a') as f:
        f.write(categoria)

def limpiar(archivo_output):
    """
    limpiar : String -> None
    Toma el nombre del archivo a escribir el output, y elimina el contenido de este.
    """
    with open(archivo_output, 'w') as f:
        f.write("")


def main():
    # Se obtiene desde la terminal el nombre de los 
    # archivos de jugadores y distancias
    archivo_jugadores, archivo_distancias = sys.argv[1:]

    # Pedimos como input el nombre del archivo de salida
    archivo_output = obtener_archivo_salida()
    
    # Obtenemos N, la distancia máxima a realizar los enfrentamientos
    N = obtener_dist_maxima()
    
    # Definimos la lista de tuplas de la forma (nombre, edad, localidad)
    jugadores = generar_elementos_archivo(archivo_jugadores, crear_jugador)

    # Reducimos la cantidad de jugadores para realizar pruebas
    jugadores = jugadores

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
    iniciar_juego("Mayores de edad", archivo_output)
    ganadores_regionales_mayores = jugada_en_misma_ciudad(ciudades,jugadores_mayores, archivo_output)
    jugada_por_regiones(ciudades, ganadores_regionales_mayores, N,distancias_localidades,archivo_output)
    
    # Realizamos la instancia de enfrentamientos de menores de edad, primero por ciudades
    # y luego, entre los ganadores se enfrentarán por regiones/ciudades, solo si se
    # encuentran en el radio permitido
    iniciar_juego("Menores de edad", archivo_output)
    ganadores_regionales_menores = jugada_en_misma_ciudad(ciudades,jugadores_menores, archivo_output)
    jugada_por_regiones(ciudades, ganadores_regionales_menores, N, distancias_localidades,archivo_output)

    print("El archivo " + archivo_output + " fue escrito.")

if __name__ == "__main__":
    main()
