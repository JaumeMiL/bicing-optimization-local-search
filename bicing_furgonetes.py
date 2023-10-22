import random

from abia_bicing import Estacion, Estaciones

def dist_estacions(est1: Estacion, est2: Estacion) -> int:
    distancia = abs(est1.coordX - est2.coordX) + abs(est1.coordY - est2.coordY)
    return distancia

class Furgonetes(object):
    def __init__(self, origen: Estacion, bicis_carregades: int = 0, primera_est: Estacion = None, bicis_primera: int = 0, segona_est: Estacion = None, bicis_segona: int = 0):
        self.origen = origen  # Estació on carrega
        self.primera_est = primera_est  # Primera estació
        self.segona_est = segona_est  # Segona estació
        self.bicis_carregades = bicis_carregades  
        self.bicis_primera = bicis_primera  # Nombre de bicis que es deixen a la primera estació
        self.bicis_segona = bicis_segona  # Nombre de bicis que es deixen a la segona estació
        if primera_est is None:
            assert bicis_primera == 0  # Si no hi ha primera estació, la quantitat de bicis ha de ser 0
        if segona_est is None:
            assert bicis_segona == 0  # Si no hi ha segona estació, la quantitat de bicis ha de ser 0
    
    def cost_gasolina(self):
            cost_gas = 0

            # Obtenim les variables necessàries
            bicis_carregades = self.bicis_carregades
            bicis_primera = self.bicis_primera 
            bicis_segona = self.bicis_segona
            origen = self.origen
            primera_est = self.primera_est
            segona_est = self.segona_est

            # si existeix la primera estació calculem el cost de la gasolina d'anar-hi
            if primera_est is not None and origen is not None and bicis_primera != 0:
                cost_gas += (((bicis_carregades + 9)//10) * dist_estacions(origen, primera_est)/1000)

                # si existeix la segona estació calculem el cost de la gasolina d'anar-hi
                if segona_est is not None and bicis_segona != 0:
                    cost_gas += (((bicis_carregades - bicis_primera + 9)//10) * dist_estacions(primera_est, segona_est)/1000)
            
            return cost_gas
    
    def ingresos(self):
        primera_est = self.primera_est
        segona_est = self.segona_est
        bicis_primera = self.bicis_primera
        bicis_segona = self.bicis_segona
        ingresos = 0

        if primera_est is not None and primera_est.num_bicicletas_next < primera_est.demanda:
            ingresos_maxims1 = (primera_est.demanda - primera_est.num_bicicletas_next) 
            ingresos += min(bicis_primera, ingresos_maxims1)
        
        if segona_est is not None and segona_est.num_bicicletas_next < segona_est.demanda: 
            ingresos_maxims2 = (segona_est.demanda - segona_est.num_bicicletas_next) 
            ingresos += min(bicis_segona,  ingresos_maxims2)
        
        return ingresos  
        
    
    def perdues(self):
        perdues = 0
        if self.origen is not None:
            origen = self.origen
            bicis_carregades = self.bicis_carregades

            if origen.num_bicicletas_next <= origen.demanda:
                perdues += bicis_carregades
            
            else:
                sobra = origen.num_bicicletas_next - origen.demanda
                if sobra < bicis_carregades:
                    perdues += bicis_carregades-sobra
            return perdues
        
    def distancia_recorreguda(self):
        dist_total = 0
        if self.primera_est is not None and self.origrn is not None:
            dist_total += dist_estacions(self.orien, self.primera_est)
            if self.segona_est is not None:
                dist_total += dist_estacions(self.primera_est, self.segona_est)
        return dist_total
    
    def __repr__(self):
        return f"Furgoneta: Origen: {self.origen}, Bicis caregades: {self.bicis_carregades},\nPrimera estació de destí: {self.primera_est}, Bicis descarregades: {self.bicis_primera},\nSegona estació de destí: {self.segona_est}, Bicis descarregades: {self.bicis_segona}\n )"
    def __eq__(self, __value: object) -> bool:
        return self.origen == __value.origen and self.bicis_carregades == __value.bicis_carregades and self.bicis_primera == __value.bicis_primera and self.bicis_segona == __value.bicis_segona and self.primera_est == __value.primera_est and self.segona_est == __value.segona_est
    def __copy__(self):
        return Furgonetes(self.origen, self.bicis_carregades, self.primera_est, self.bicis_primera, self.segona_est , self.bicis_segona)
