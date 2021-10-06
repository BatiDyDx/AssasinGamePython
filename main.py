
import random
import sys


def obtener_n():
    return float(input("Ingrese la distancia maxima: "))


def crear_jugador(strline):
    nombre, edad, localidad = strline.split(',')
    edad = int(edad)
    return (nombre, edad, localidad)


def crear_localidad(strline):
    localidad1, localidad2, distancia = strline.split(',')
    distancia = float(distancia)
    return (localidad1, localidad2, distancia)


def separar_edades(jugadores):
    menores = filter(lambda jugador: (jugador[3] <= 17),jugadores)
    mayores = filter(lambda jugador: (jugador[3] > 17),jugadores)
    return menores, mayores


def generar_lista_de_txt(file, funcion_generar):
    lista = []
    with open(file, 'r') as f:
        for line in f.read_lines():
            elemento = funcion_generar(line)
            lista.append(elemento)
    return lista


def jugada(jugador1, jugador2):
    return random.choice([jugador1,jugador2])


def distancia_valida(n, jugador1, jugador2):
    dist = distancia(jugador1[3], jugador2[3])
    return dist < n


def main():
    file_jugadores, file_distancias = sys.args()
    n = obtener_n()
