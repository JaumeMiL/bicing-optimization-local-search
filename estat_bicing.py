import random
from abia_bicing import *
class Estat:
    def __init__(self, num_estacions, num_bicis, semilla, num_furgos):
        self.estacions = Estaciones(num_estacions, num_bicis, semilla)
        self.visitat = [False] * num_estacions
        self.furgonetes = [Furgoneta(i) for i in range(1, num_furgos+1)]
        self.costos = 0
        self.beneficis = 0
        
    def calcular_distancia_entre_estacions(self, estacio1, estacio2):
        x1, y1 = estacio1.coordX, estacio1.coordY
        x2, y2 = estacio2.coordX, estacio2.coordY
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distancia
        
    def moure_bicis(self,origen,arribada1,arribada2):
        furgoneta = self.furgonetes[origen-1]
        
        if arribada2 is None:  # Si sol es va a una estació
            bicis_a_enviar = min(furgoneta.capacitat, self.estacions.lista_estaciones[origen].num_bicicletas_next)
            furgoneta.capacitat -= bicis_a_enviar
            self.estacions.lista_estaciones[origen].num_bicicletas_next -= bicis_a_enviar
            self.estacions.lista_estaciones[arribada1].num_bicicletas_no_usadas += bicis_a_enviar
            
            distancia = self.calcular_distancia_entre_estacions(self.estacions.lista_estaciones[origen], self.estacions.lista_estaciones[arribada1])
            self.costos += ((bicis_a_enviar + 9) // 10)*distancia
            
        else:  # Si n'hi ha dos
            demanda_arribada1 = self.estacions.lista_estaciones[arribada1].demanda
            demanda_arribada2 = self.estacions.lista_estaciones[arribada2].demanda
            
            bicis_a_enviar_arribada1 = min(furgoneta.capacitat, demanda_arribada1)
            bicis_a_enviar_arribada2 = min(furgoneta.capacitat - bicicletas_a_enviar_arribada1, demanda_arribada2)
            
            furgoneta.capacitat -= (bicis_a_enviar_arribada1 + bicis_a_enviar_arribada2)
            self.estacions.lista_estaciones[origen].num_bicicletas_next -= (bicis_a_enviar_arribada1 + bicis_a_enviar_arribada2)
            self.estacions.lista_estaciones[arribada1].num_bicicletas_no_usadas += bicis_a_enviar_arribada1
            self.estacions.lista_estaciones[arribada2].num_bicicletas_no_usadas += bicis_a_enviar_arribada2
            
            distancia1 = self.calcular_distancia_entre_estacions(self.estacions.lista_estaciones[origen], self.estacions.lista_estaciones[arribada1])
            distancia2 = self.calcular_distancia_entre_estacions(self.estacions.lista_estaciones[arribada1], self.estacions.lista_estaciones[arribada2])
            self.costos +=  ((bicis_a_enviar_arribada1 + 9) // 10)*distancia1
            self.costos +=  ((bicis_a_enviar_arribada1 + 9) // 10)*distancia2
        
        self.visitat[origen] = True


class Furgoneta:
    
    def __init__(self,origen):
        self.origen = origen
        self.capacitat = 30
        
    
