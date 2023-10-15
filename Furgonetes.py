from abia_bicing import *
from estat_bicing import *

def distancia_estacions(est1: Estacion, est2: Estacion) -> int:
    distancia = abs(est1.coordX - est2.coordX) + abs(est1.coordY - est2.coordY)
    return distancia

class Furgonetes(object):

    def __init__(self, origen: Estacion, bicis_furgo: int, primera_est: Estacion = None, bicis_primera: int = 0, segona_est: Estacion = None, bicis_segona: int = 0):
        self.origen = origen  # Estació on carrega
        self.primera_est = primera_est  # Primera estació
        self.segona_est = segona_est  # Segona estació
        self.bicis_furgo = bicis_furgo  # Nombre de bicis que porta a sobre
        self.bicis_primera = bicis_primera  # Nombre de bicis que es deixen a la primera estació
        self.bicis_segona = bicis_segona  # Nombre de bicis que es deixen a la segona estació

        if primera_est is None:
            assert bicis_primera == 0  # Si no hi ha primera estació, la quantitat de bicis ha de ser 0

        if segona_est is None:
            assert bicis_segona == 0  # Si no hi ha segona estació, la quantitat de bicis ha de ser 0

    
    def cost_gasolina(self):
        cost_gas = 0

        # Obtenim les variables necessàries
        bicis_furgo = self.bicis_furgo
        origen = self.origen
        primera_est = self.primera_est
        segona_est = self.segona_est

        # si existeix la primera estació calculem el cost de la gasolina d'anar-hi
        if primera_est is not None:
            cost_gas += ((bicis_furgo + 9)//10) * distancia_estacions(origen, primera_est)/1000

            # si existeix la segona estació calculem el cost de la gasolina d'anar-hi
            if segona_est is not None:
                cost_gas += ((bicis_furgo - self.bicis_primera + 9)//10) * distancia_estacions(primera_est, segona_est)/1000

        return cost_gas

