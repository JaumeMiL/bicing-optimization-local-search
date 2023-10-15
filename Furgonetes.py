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
        carrega = self.carrega
        descarrega1 = self.descarrega1
        descarrega2 = self.descarrega2
        estacio_carrega = self.estacio_carrega
        estacio_descarrega1 = self.estacio_descarrega1
        estacio_descarrega2 = self.estacio_descarrega2

        if estacio_descarrega1 is not None:
            cost_1 = ((carrega + 9) // 10) * (distancia_estacions(estacio_carrega, estacio_descarrega1) / 1000)
            cost_total += cost_1
            
            if estacio_descarrega2 is not None:
                cost_2 = (((carrega - descarrega1) + 9) // 10) * (distancia_estacions(estacio_descarrega1, estacio_descarrega2) / 1000)
                cost_total += cost_2
                
        return cost_total
    
    def guanys(self):
        estacio_descarrega1 = self.estacio_descarrega1
        estacio_descarrega2 = self.estacio_descarrega2
        descarrega1 = self.descarrega1
        descarrega2 = self.descarrega2
        guanys = 0

        if estacio_descarrega1 is not None and estacio_descarrega1.num_bicicletas_next < estacio_descarrega1.demanda:
            possibles_guanys = (estacio_descarrega1.demanda - estacio_descarrega1.num_bicicletas_next) 
            guanys += min(descarrega1,  possibles_guanys)
        if estacio_descarrega2 is not None and estacio_descarrega2.num_bicicletas_next < estacio_descarrega2.demanda: 
            possibles_guanys2 = (estacio_descarrega2.demanda - estacio_descarrega2.num_bicicletas_next) 
            guanys += min(descarrega2,  possibles_guanys2)
        return guanys  
        
    
    def perdues(self):
        estacio_carrega = self.estacio_carrega
        carrega = self.carrega
        perdues = 0
        if estacio_carrega.num_bicicletas_next <= estacio_carrega.demanda:
            perdues += carrega
        else:
            sobrants = estacio_carrega.num_bicicletas_next - estacio_carrega.demanda
            if sobrants < carrega:
                perdues += carrega-sobrants
        return perdues
    def __repr__(self):
        return f"Furgonetes({self.estacio_carrega}, {self.carrega}, {self.estacio_descarrega1}, {self.descarrega1}, {self.estacio_descarrega2}, {self.descarrega2})"

        
    
