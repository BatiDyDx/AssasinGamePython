from main import *
import random

random.seed(10000) # Definimos una seed para poder testear las funciones que dependen de random


def test_crear_jugador():
    assert crear_jugador("JOSE DELGADO,51,Rosario\n") == ("JOSE DELGADO", 51, "Rosario")
    assert crear_jugador("MANUEL JIMENEZ,46,Villa Maria\n") == ("MANUEL JIMENEZ", 46, "Villa Maria")
    assert crear_jugador("NORA DURAN,28,CABA\n") == ("NORA DURAN", 28, "CABA")


def test_crear_dist_localidades():
    assert crear_dist_localidades("Cordoba, Villa Gobernador Galvez, 410.3") == ("Cordoba", "Villa Gobernador Galvez", 410.3)
    assert crear_dist_localidades("Santa Fe, Villa Maria, 302.7") == ("Santa Fe", "Villa Maria", 302.7)
    assert crear_dist_localidades("Rio Cuarto, Serodino, 388.7") == ("Rio Cuarto", "Serodino", 388.7)


def test_obtener_lista_ciudades():
    distancias = [
                ("CABA", "Rosario", 299.9),
                ("Rosario", "Villa Constitucion", 59.7),
                ("Parana", "Tierra del Fuego", 3278.8)
                ]
    assert obtener_set_ciudades(distancias) == {"CABA", "Rosario", "Villa Constitucion", "Parana", "Tierra del Fuego"}


def test_distancia_valida():
    N = 250
    #distancias = obtener()
    distancia_valida(N, )

