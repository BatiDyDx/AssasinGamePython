from main import *

def test_crear_jugador():
    assert crear_jugador("JOSE DELGADO,51,Rosario\n") == ("JOSE DELGADO", 51, "Rosario")
    assert crear_jugador("MANUEL JIMENEZ,46,Villa Maria\n") == ("MANUEL JIMENEZ", 46, "Villa Maria")
    assert crear_jugador("NORA DURAN,28,CABA\n") == ("NORA DURAN", 28, "CABA")


def test_crear_dist_localidades():
    assert crear_dist_localidades("Cordoba, Villa Gobernador Galvez, 410.3") == ("Cordoba", "Villa Gobernador Galvez", 410.3)
    assert crear_dist_localidades("Santa Fe, Villa Maria, 302.7") == ("Santa Fe", "Villa Maria", 302.7)
    assert crear_dist_localidades("Rio Cuarto, Serodino, 388.7") == ("Rio Cuarto", "Serodino", 388.7)


def test_separar_edades():
    jugadores = [("Juan", 12, "Rosario"), ("Rodofredo", 40, "Calafate"), ("Nicolas", 17, "CABA")]
    menores = [("Juan", 12, "Rosario"), ("Nicolas", 17, "CABA")]
    mayores = [("Rodofredo", 40, "Calafate")]
    assert separar_edades(jugadores) == (menores, mayores)


def test_generar_lista_jugadores():
    jugadores = [
        ("MARIA EUGENIA PORRAS", 72, "Serodino"), 
        ("CARMEN CORRALES", 75, "Santa Fe"),
        ("ROXANA MARIA MIRANDA", 90, "Rio Cuarto"),
        ("MARTA VILLALTA", 95, "Rosario")
    ]

    assert generar_lista_jugadores("TestJug.txt") == jugadores


def test_generar_dict_distancias():
    dict_ciudades_distancia = {
        ("CABA", "Cordoba"): 696.4,
        ("CABA", "Rio Cuarto"): 617.8,
        ("CABA", "Rosario"): 299.9
    }
    assert generar_dict_distancias("TestDist.txt") == dict_ciudades_distancia


def test_obtener_dist_localidades():
    dict_dist = {
        ("CABA", "Cordoba"): 696.4, 
        ("Santa Fe", "Villa Constitucion"): 228.3, 
        ("CABA", "Rosario"): 299.9
    }
    assert obtener_dist_localidades(dict_dist, "CABA", "Cordoba") == 696.4
    assert obtener_dist_localidades(dict_dist, "Rosario", "CABA") == 299.9
    assert obtener_dist_localidades(dict_dist, "Villa Constitucion", "Santa Fe") == 228.3


def test_distancia_valida():
    dict_dist = {
        ("CABA", "Cordoba"): 696.4, 
        ("Santa Fe", "Villa Constitucion"): 228.3, 
        ("CABA", "Rosario"): 299.9
    }
    assert distancia_valida(700, dict_dist, "CABA", "Cordoba") == True
    assert distancia_valida(200, dict_dist, "Rosario", "CABA") == False
    assert distancia_valida(200, dict_dist, "Villa Constitucion", "Santa Fe") == False


def test_obtener_set_ciudades():
    dict_dist = {
        ("Serodino", "Villa Maria"): 255.1,
        ("Rio Cuarto", "Santa Fe"): 433.6,
        ("Parana", "Tierra del Fuego") : 3278.8
    }
    assert obtener_set_ciudades(dict_dist) == set(("Serodino", "Villa Maria", "Rio Cuarto", "Santa Fe", "Parana", "Tierra del Fuego"))


def test_obtener_jugadores_por_ciudad():
    set_ciudades = set(("CABA","Rio Cuarto","Rosario"))
    jugadores = [
        ("ROBERTO ALMEIDO",20,"Rosario"),
        ("JUAN MANUEL",5,"Rio Cuarto"),
        ("JOSE MIGUEL",1,"CABA"),
        ("MARIA EUGENIA PADILLA",70,"CABA"),
        ("OLGA ARGUEDAS",66,"Rio Cuarto")
    ]
    dict_jugadores_ciudad = {
        "CABA": [("JOSE MIGUEL",1,"CABA"), ("MARIA EUGENIA PADILLA",70,"CABA")],
        "Rio Cuarto": [("JUAN MANUEL",5,"Rio Cuarto"),("OLGA ARGUEDAS",66,"Rio Cuarto")],
        "Rosario": [("ROBERTO ALMEIDO",20,"Rosario")]
    }
    assert obtener_jugadores_por_ciudad(jugadores,set_ciudades) == dict_jugadores_ciudad


def test_jugador_mas_cercano():
    jugador1 = ("CECILIA MORA", 91, "Rosario")
    peleadores_potenciales = [
        ("OLGA MARIA CASTRO", 58, "Villa Constitucion"),
        ("EVELIO ELIZONDO", 17, "Cordoba"),
        ("ARTURO ORLANDO ROJAS", 81, "CABA"),
        ("GRACIELA BRENES", 93, "Villa Gobernador Galvez")
    ]

    dict_ciudades_distancia = {
        ("Rosario", "Villa Constitucion"): 59.7,
        ("Cordoba", "Rosario"): 400.9,
        ("CABA", "Rosario"): 299.9,
        ("Rosario", "Villa Gobernador Galvez"): 13.9
    }
    assert jugador_mas_cercano(jugador1, peleadores_potenciales, dict_ciudades_distancia) == ("GRACIELA BRENES", 93, "Villa Gobernador Galvez")


def test_duelo():
    jugador1, jugador2 = ("OMAR MORA", 76, "CABA"), ("FRANCISCO SEAS", 31, "Cordoba")
    ganador, perdedor = duelo(jugador1, jugador2)
    assert (jugador1, jugador2) == (ganador, perdedor) or (jugador1, jugador2) == (perdedor, ganador)
