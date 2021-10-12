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

def test_separar_edades():
    assert separar_edades([("juan",2,"rosario"),("rodofredo",40,"calafate")]) == [("juan",2,"rosario")],[("rodofredo",40,"calafate")]

def test_generar_lista_jugadores():
    assert generar_lista_jugadores("TestJug.txt") == []

def test_generar_dict_distancias():
    assert generar_dict_distancias("TestDist.txt") == {("CABA","Cordoba"):696.4,("CABA","Rio Cuarto"):617.8,("CABA","Rio Cuarto"):299.9}

def test_obtener_dist_localidades():
    dict_dist = {("CABA","Cordoba"):696.4,("CABA","Rio Cuarto"):617.8,("CABA","Rosario"):299.9}
    assert obtener_dist_localidades(dict_dist,"CABA","Cordoba") == 696.4
    assert obtener_dist_localidades(dict_dist,"CABA","Rosario") == 299.9
    #assert obtener_dist_localidades(dict_dist,"CABA","San Juan") == 696.4

def test_distancia_valida():
    dict_dist = {("CABA","Cordoba"):696.4,("CABA","Rio Cuarto"):617.8,("CABA","Rosario"):299.9}
    assert distancia_valida(700,dict_dist,"CABA","Cordoba") == True
    assert distancia_valida(200,dict_dist,"CABA","Rosario") == False
    assert distancia_valida(200,dict_dist,"CABA","Rio Cuarto") == True

def test_obtener_set_ciudades():
    dict_dist = {("CABA","Cordoba"):696.4,("CABA","Rio Cuarto"):617.8,("CABA","Rosario"):299.9}
    assert obtener_set_ciudades(dict_dist) == set("CABA","Rio Cuarto","Rosario")

def test_obtener_jugadores_por_ciudad():
    set_ciudades = set("CABA","Rio Cuarto","Rosario")
    jugadores = [("ROBERTO ALMEIDO",20,"Rosario"),("JUAN MANUEL",5,"Rio Cuarto"),("JOSE MIGUEL",1,"CABA")]
    assert obtener_jugadores_por_ciudad(jugadores,set_ciudades) == {"CABA":[("JOSE MIGUEL",1,"CABA")],"Rio Cuarto":[("JUAN MANUEL",5,"Rio Cuarto")],"Rosario":[("ROBERTO ALMEIDO",20,"Rosario")]}

def test_jugador_mas_cercano():
    pass


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

