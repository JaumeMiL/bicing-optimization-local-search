from abia_bicing import Estacion

def calcular_distancia(estacio_a: Estacion, estacio_b: Estacion) -> int:
    return (abs(estacio_a.coordX - estacio_b.coordX) + abs(estacio_a.coordY - estacio_b.coordY))