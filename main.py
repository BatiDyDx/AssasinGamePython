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
    nombre_archivo = input("Ingrese un nombre para el archivo de salida: (por defecto es " + valor_defecto + "): ")
    # Si el usuario no introduce ningun valor, retornamos el valor por defecto
    if nombre_archivo == "":
        nombre_archivo = valor_defecto
    return nombre_archivo


def crear_jugador(linea):
    """
    crear_jugador : String -> Tuple(String, Int, String)
    crear_jugador toma una linea de texto, con formato
    nombre,edad,localidad; y devuelve una tupla de la forma
    (nombre, edad, localidad)
    """
    nombre, edad, localidad = linea.split(',')
    # Quitamos el caracter \n de localidad
    localidad = localidad[:-1]
    # Convertimos la edad a un int
    edad = int(edad)
    return (nombre, edad, localidad)


def crear_dist_localidades(linea):
    """
    crear_dist_localidades : String -> Tuple(String, String, Float)
    crear_dist_localidades toma una linea de texto, con formato
    localidad1, localidad2, distancia_entre_localidades, y devuelve
    una tupla de la forma (localidad1, localidad2, distancia_entre_localidades)
    """
    localidad1, localidad2, distancia = linea.split(',')
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


def generar_lista_jugadores(archivo):
    """
    generar_lista_jugadores : String -> List(Tuple(String, Int, String))
    generar_lista_jugadores tome el nombre de un archivo de donde leer,
    y pasa cada linea por la funcion crear_jugador, lo agrega a una lista,
    y retorna esta ultima
    """
    jugadores = []
    with open(archivo, 'r') as f:
        # Para cada linea del archivo de entrada leemos
        for linea in f.readlines():
            # Pasamos la linea leida del archivo a la funcion crear_jugador
            jugador = crear_jugador(linea)
            # Agreagamos al jugador a la lista
            jugadores.append(jugador)
    return jugadores


def generar_dict_distancias(archivo):
    """
    generar_elementos_archivo : String -> Dict(Tuple(String, String) : Float)
    generar_elementos_archivo toma un string que representa
    el nombre del archivo de donde leer las distancias, y devuelve un diccionario
    donde la llave es una tupla con las dos ciudades (los elementos de la tupla están
    ordenado alfaeticamente), y el valor es la distancia correspondiente a las
    correspondientes localidades
    """
    dict_ciudades_distancia = {}
    with open(archivo, 'r') as f:
        # Para cada linea del archivo de entrada leemos
        for linea in f.readlines():
            # Pasamos la linea leida del archivo a la funcion generadora
            # la cual se debe encargar de interpretar el string linea y
            # generar una tupla de la forma (localidad1, localidad2, distancia)
            tupla_ciudades_distancia = crear_dist_localidades(linea)
            # El par_ciudades es una tupla (localidad1, localidad2) ordenada
            # alfabeticamente
            par_ciudades = tuple(sorted(tupla_ciudades_distancia[:2]))
            # Agregamos como llave al diccionario la tupla par_ciudades,
            # cuyo valor es la distancia correspondiente
            dict_ciudades_distancia[par_ciudades] = tupla_ciudades_distancia[2]
    return dict_ciudades_distancia


def duelo(jugador1, jugador2):
    """
    duelo : Tuple(String, Int, String) Tuple(String, Int, String) -> List(Tuple(String, Int, String) Tuple(String, Int, String))
    duelo recibe dos jugadores, y devuelve una lista con los dos elementos en orden
    aleatorio. El primer elemento de la lista será interpretado como el ganador, y
    el segundo como el perdedor
    """
    peleadores = [jugador1, jugador2]
    # Mezclamos la lista
    random.shuffle(peleadores)
    return peleadores


def obtener_dist_localidades(dict_ciudades_distancias, localidad1, localidad2):
    """
    obtener_dist_localidades : Dict(Tuple(String, String) : Float) String String -> Float
    obtener_dist_localidades recibe un diccionario (que representa las distancias entre las ciudades), 
    y dos ciudades, y retorna la distancia entre estas
    """
    # Si las localidades a comparar son la misma, la distancia entre
    # ellas es trivialmente 0
    if localidad1 == localidad2:
        return 0.0
    else:
        # Definimos una tupla ordenada con los nombres de las ciudades
        par_localidades = tuple(sorted((localidad1, localidad2)))
        try:
            # Probamos si la tupla se encuentra en el diccionario
            distancia_localidades = dict_ciudades_distancias[par_localidades]
        except KeyError:
            # Si la tupla no está en el diccionario, significa que la distancia
            # entre ambas ciudades no fue declarada en el archivo de texto proveido
            # como input del programa, por lo que levantamos un error
            msg_error = "El par de ciudades "
            msg_error += str(par_localidades)
            msg_error += " no se encuentra en el archivo de distancias proveido, por lo que no se puede conocer la distancia entre ellas"
            raise RuntimeError(msg_error)
        else:
            # Retornamos el valor del diccionario correspondiente a la tupla,
            # la cual sabemos que debe estar, ya que las llaves en el diccionario
            # distancias estan ordenadas
            return distancia_localidades

def distancia_valida(distancia_maxima, dict_ciudades_distancia, ciudad1, ciudad2):
    """
    distancia_valida : Float Dict(Tuple(String, String) : Float) String String -> Bool
    distancia_valida determina si dos ciudades estan a una distancia válida dado un número n
    """
    #Se consigue la distancia entre 2 ciudades
    dist = obtener_dist_localidades(dict_ciudades_distancia, ciudad1, ciudad2)
    #Se chequea si esta dentro del N especificado
    #devolviendo un valor True or False
    return dist < distancia_maxima


def obtener_set_ciudades(dict_ciudades_distancias):
    """
    obtener_set_ciudades : Dict(Tuple(String, String) : Float) -> Set(String)
    obtener_set_ciudades recibe un diccionario (que representan distancias entre
    pares de ciudades), y retorna un set con los nombres de todas las ciudades que entran
    en el juego.
    """
    ciudades = set()
    #Se itera sobre el diccionario entregrado, y se asigna cada valor de la tupla
    #a una variable diferente
    for ciudad1, ciudad2 in dict_ciudades_distancias.keys():
        #se añaden las 2 ciudades a un conjunto
        ciudades.add(ciudad1)
        ciudades.add(ciudad2)
    return ciudades


def obtener_jugadores_por_ciudad(jugadores, conjunto_ciudades):
    """
    obtener_jugadores_por_ciudad : List(Tuple(String, Int, String)) Set(String) -> Dict(String : List(Tuple(String, Int, String)))
    obtener_jugadores_por_ciudad toma una lista de jugadores, y un conjunto de nombres
    de ciudades, y devuelve un diccionario, donde las llaves corresponden a ciudades, y los valores
    son las listas de jugadores que se encuentran en la respectiva ciudad.
    """
    dict_ciudad_jugadores = dict() 
    # Recorremos sobre las ciudades en el conjunto de ciudades
    for ciudad in conjunto_ciudades:
        # Agregamos al diccionario como llave el valor de una ciudad,
        # y el valor corresponde a la lista de jugadores en dicha ciudad
        dict_ciudad_jugadores[ciudad] = list(filter(lambda jugador: (jugador[2] == ciudad), jugadores))
    return dict_ciudad_jugadores


def jugada_por_localidad(jugadores, conjunto_ciudades, archivo_output):
    """
    jugada_por_localidad : List(Tuple(String, Int, String)) Set(String) String -> List(Tuple(String, Int, String))
    jugada_por_localidad toma un conjunto de nombres de ciudades, una lista de jugadores, y el nombre
    del archivo a escribir el output, simula las peleas entre los jugadores en sus respectivas
    localidades, y devuelve la lista de jugadores que ganaron en sus respectivas localidades.
    """
    # ganadores_regionales será una lista de los jugadores que hayan ganado
    # en sus respectivas localidades
    ganadores_regionales = []

    # dict_ciudad_jugadores es un diccionario donde la llave es un string con el nombre
    # de una ciudad, y el valor es una lista de tuplas (que represenentan jugadores)
    # de los jugadores de dicha ciudad
    dict_ciudad_jugadores = obtener_jugadores_por_ciudad(jugadores, conjunto_ciudades)

    # cant_ciudades_con_ganador será el contador de ciudades que ya tienen un ganador
    cant_ciudades_con_ganador = 0
    copia_jugadores = jugadores[:]
    
    # Recorremos sobre las ciudades
    for ciudad in dict_ciudad_jugadores:
        # Si la cantidad de jugadores en la ciudad es menor o igual a
        # 1, significa que tenemos 1 ganador o ningun jugador en la ciudad,
        # por lo que incrementamos el contador de ciudades con ganador en 1
        if len(dict_ciudad_jugadores[ciudad]) <= 1:
            cant_ciudades_con_ganador += 1

            # Si hay solo un jugador, lo añadimos como ganador de se región
            if len(dict_ciudad_jugadores[ciudad]) == 1:
                ganadores_regionales.append(dict_ciudad_jugadores[ciudad][0])

    with open(archivo_output, "a") as f:
        # Mientras la cantidad de ciudades con ganador sea menor a la cantidad
        # de ciudades, significa que habrá ciudades por disputar un ganador todavia
        while cant_ciudades_con_ganador < len(conjunto_ciudades):
            # Elegimos un jugador aleatorio de la copia de la lista de jugadores totales
            jugador1 = random.choice(copia_jugadores)
            # Obtenemos la localidad del jugador elegido
            ciudad_de_jugador = jugador1[2]
            # Obtenemos los jugadores en la misma localidad del jugador elegido
            jugadores_en_ciudad = dict_ciudad_jugadores[ciudad_de_jugador]
            if len(jugadores_en_ciudad) > 1:
                # Quitamos al jugador elegido de la lista de jugadores de su localidad
                jugadores_en_ciudad.remove(jugador1)
                # Elegimos otro jugador aleatorio de la misma localidad
                jugador2 = random.choice(jugadores_en_ciudad)
                # Y removemos este jugador tambien
                jugadores_en_ciudad.remove(jugador2)
                # Se genera un ganador y un perdedor de entre los elegidos
                ganador, perdedor = duelo(jugador1, jugador2)
                # Agregamos de nuevo al ganador a la lista de jugadores de su localidad
                jugadores_en_ciudad.append(ganador)
                # Removemos al perdedor de la lista total de jugadores
                copia_jugadores.remove(perdedor)
                # Escribimos la información de la jugada en el archivo del output
                linea = ganador[0] + " eliminó a " + perdedor[0] + "\n"
                f.write(linea)
                # Si ahora la cantidad de jugadores en la localidad es 1, significa que
                # tenemos ganador
                if len(jugadores_en_ciudad) == 1:
                    # Incrementamos la cantidad de ciudades con ganador
                    cant_ciudades_con_ganador += 1
                    # Agregamos al ganador a la lista de ganadores regionales
                    ganadores_regionales.append(ganador)
    return ganadores_regionales


def jugada_entre_regiones(ganadores_regionales, conjunto_ciudades, distancia_maxima, dict_ciudades_distancia, archivo_output):
    """
    jugada_entre_regiones : List(Tuple(String, Int, String)) Set(String) Float Dict(Tuple(String, String) : Float) String -> None
    jugada_entre_regiones simula los enfrentamientos de los ganadores_regionales, siempre y cuando esten dentro del rango
    permitido, y escribe la informacion de los enfrentamientos al archivo de salida. Tambien escribe al archivo de salida
    quien es el ganador, o ganadores en caso de haberlos.
    """
    ganadores_locales = []
    ganadores_copia = ganadores_regionales[:]

    # Si en la lista de ganadores regionales hay
    # solo un jugador, ese será el ganador
    if len(ganadores_regionales) == 1:
        ganador = ganadores_regionales[0]

    f = open(archivo_output, "a")

    # Si tenemos N jugadores, realizaremos N - 1 enfrentamientos
    for _ in range(len(ganadores_copia) - 1):
        peleadores_potenciales = []
        # Elejimos el primer jugador de los ganadores regionales
        jugador1 = random.choice(ganadores_copia)

        # Obtenemos la lista de ciudades dentro de la distancia maxima
        ciudades_cercanas = list(filter(lambda ciudad: distancia_valida(distancia_maxima, dict_ciudades_distancia, jugador1[2], ciudad), conjunto_ciudades))
        
        # Iteramos sobre la lista de jugadores
        for peleador in ganadores_copia:
            # Si el jugador reside en una de las ciudades dentro del limite
            # la agregamos como posible rival para el jugador 1
            if peleador[2] in ciudades_cercanas and peleador != jugador1:
                peleadores_potenciales.append(peleador)

        # Si no hay jugadores cercanos se lo toma al jugador 1 como ganador de su region
        if peleadores_potenciales == []:
            ganadores_locales.append(jugador1)
            ganadores_copia.remove(jugador1)
        else:
            # Se elije el jugador 2 como el más cercano de entre los peleadores potenciales
            jugador2 = jugador_mas_cercano(jugador1,peleadores_potenciales,dict_ciudades_distancia)
            # Se genera un ganador y un perdedor de entre los elegidos
            ganador, perdedor = duelo(jugador1, jugador2)
            #Removemos el perdedor de los jugadores restantes
            ganadores_copia.remove(perdedor)
            # Escribimos la información de la jugada en el archivo del output
            linea = ganador[0] + " eliminó a " + perdedor[0] + "\n"
            f.write(linea)
    f.close()
    #Si no tenemos ganadores locales, eso nos dice que hay un solo ganador
    if ganadores_locales == []:
        anunciar_ganador(ganador, archivo_output)
    #Sino, se anuncian varios ganadores regionales
    else:
        anunciar_varios_ganadores(ganadores_locales, archivo_output)


def jugador_mas_cercano(jugador1, peleadores_potenciales, dict_ciudades_distancia):
    """
    jugador_mas_cercano : Tuple(String,Int,String) List(Tuple(String,Int,String)) Dict{(String,String) : Float}
    -> Tuple(String,Int,String)
    Recibe el jugador, sus posibles jugadores y el diccionario de distancias
    y devuelve el que esta a menor distancia del jugador
    """
    dict_jugadores_dist = dict()
    # Itera sobre todos los jugadores potenciales
    for jugador in peleadores_potenciales:
        # Guarda la distancia de jugador en un variable
        distancia = obtener_dist_localidades(dict_ciudades_distancia,jugador1[2],jugador[2])
        # Añade a un diccionario con la clave del jugador y como valor la distancia
        dict_jugadores_dist[jugador] = distancia 
    # Devuelve el elemento con el valor mas chico en el diccionario
    jugador_mas_cercano = min(dict_jugadores_dist, key = dict_jugadores_dist.get)
    return jugador_mas_cercano


def anunciar_ganador(ganador, archivo_output,):
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


def anunciar_categoria(categoria, archivo_output):
    """
    anunciar_categoria : String String -> None
    Toma una categoria de jugadores y el nombre del archivo a escribir
    el output, y escribe la categoria a que va a jugar
    """
    with open(archivo_output, 'a') as f:
        f.write(categoria + '\n')


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
    
    # Obtenemos la distancia máxima a realizar los enfrentamientos
    distancia_maxima = obtener_dist_maxima()
    
    # Definimos la lista de tuplas de la forma (nombre, edad, localidad)
    jugadores = generar_lista_jugadores(archivo_jugadores)

    # Reducimos la cantidad de jugadores para realizar pruebas
    #jugadores = jugadores

    # Separamos la lista de jugadores entre los que son menores y mayores de edad
    jugadores_menores, jugadores_mayores = separar_edades(jugadores)

    # Obtenemos el diccionario {(localidad1, localidad2) : distancia}
    distancias_localidades = generar_dict_distancias(archivo_distancias)

    # Definimos un set con todos los nombres de las distintas ciudades
    conjunto_ciudades = obtener_set_ciudades(distancias_localidades)

    # Limpiamos el archivo que se usará de output
    limpiar(archivo_output)

    # Realizamos la instancia de enfrentamientos de mayores de edad, primero por ciudades
    # y luego, entre los ganadores se enfrentarán por regiones/ciudades, solo si se
    # encuentran en el radio permitido
    anunciar_categoria("Mayores de edad", archivo_output)
    ganadores_regionales_mayores = jugada_por_localidad(jugadores_mayores, conjunto_ciudades, archivo_output)
    jugada_entre_regiones(ganadores_regionales_mayores, conjunto_ciudades, distancia_maxima, distancias_localidades, archivo_output)
    
    # Realizamos la instancia de enfrentamientos de menores de edad, primero por ciudades
    # y luego, entre los ganadores se enfrentarán por regiones/ciudades, solo si se
    # encuentran en el radio permitido
    anunciar_categoria("Menores de edad", archivo_output)
    ganadores_regionales_menores = jugada_por_localidad(jugadores_menores, conjunto_ciudades, archivo_output)
    jugada_entre_regiones(ganadores_regionales_menores, conjunto_ciudades, distancia_maxima, distancias_localidades, archivo_output)

    # Avisamos que el output ha sido escrito
    print("El archivo " + archivo_output + " fue escrito.")

if __name__ == "__main__":
    main()
