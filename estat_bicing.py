import random
from copy import deepcopy
from abia_bicing import *
class Estat:
    def __init__(self, num_estacions, num_bicis, semilla, num_furgos):
        self.estacions = Estaciones(num_estacions, num_bicis, semilla)
        self.visitat = [False] * num_estacions
        self.furgonetes = [Furgoneta(i) for i in range(1, num_furgos+1)]
        self.guanyat = 0
        
    def calcular_distancia_entre_estacions(self, estacio1, estacio2):
        x1, y1 = estacio1.coordX, estacio1.coordY
        x2, y2 = estacio2.coordX, estacio2.coordY
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distancia
        
def moure_bicis(self, origen, arribada1, arribada2=None):
    furgoneta = self.furgonetes[origen]
    
    # Funció auxiliar per calcular si ens apropem a deixar més o menys bicis, si sumem beneficis o costos beneficios o costos
    def benefici_o_cost(estacion, bicis_a_enviar):
        diferencia = estacion.num_bicicletas_next + bicis_a_enviar - estacion.demanda
        if diferencia <= 0:
            return -diferencia  #Benefici
        else:
            return diferencia  #Cost

    # Sol es va a una estació
    if arribada2 is None:
        bicis_a_enviar = min(furgoneta.capacitat, self.estacions.lista_estaciones[origen].num_bicicletas_next)
        self.guanyat += benefici_o_cost(self.estacions.lista_estaciones[arribada1], bicis_a_enviar)
        
        # Actualitzem la furgoneta i estació
        furgoneta.capacitat -= bicis_a_enviar
        furgoneta.destins.append(arribada1)
        furgoneta.bicis_per_desti[arribada1] = bicis_a_enviar
        self.estacions.lista_estaciones[origen].num_bicicletas_next -= bicis_a_enviar
        self.estacions.lista_estaciones[arribada1].num_bicicletas_no_usadas += bicis_a_enviar
        
        # Calcular cost pr distancia
        distancia = self.calcular_distancia_entre_estacions(self.estacions.lista_estaciones[origen], self.estacions.lista_estaciones[arribada1])
        self.guanyat -= ((bicis_a_enviar + 9) // 10)*distancia

    else:  # Si es va a dos estacions
        demanda_arribada1 = self.estacions.lista_estaciones[arribada1].demanda
        demanda_arribada2 = self.estacions.lista_estaciones[arribada2].demanda
        
        bicis_a_enviar_arribada1 = min(furgoneta.capacitat, demanda_arribada1)
        bicis_a_enviar_arribada2 = min(furgoneta.capacitat - bicis_a_enviar_arribada1, demanda_arribada2)
        
        self.guanyat += benefici_o_cost(self.estacions.lista_estaciones[arribada1], bicis_a_enviar_arribada1)
        self.guanyat += benefici_o_cost(self.estacions.lista_estaciones[arribada2], bicis_a_enviar_arribada2)
        
        # Actualitzar furgoneta i estacions
        furgoneta.capacitat -= (bicis_a_enviar_arribada1 + bicis_a_enviar_arribada2)
        furgoneta.destins.extend([arribada1, arribada2])
        furgoneta.bicis_per_desti[arribada1] = bicis_a_enviar_arribada1
        furgoneta.bicis_per_desti[arribada2] = bicis_a_enviar_arribada2
        self.estacions.lista_estaciones[origen].num_bicicletas_next -= (bicis_a_enviar_arribada1 + bicis_a_enviar_arribada2)
        self.estacions.lista_estaciones[arribada1].num_bicicletas_no_usadas += bicis_a_enviar_arribada1
        self.estacions.lista_estaciones[arribada2].num_bicicletas_no_usadas += bicis_a_enviar_arribada2
        
        # Calcular cost per distancia
        distancia1 = self.calcular_distancia_entre_estacions(self.estacions.lista_estaciones[origen], self.estacions.lista_estaciones[arribada1])
        distancia2 = self.calcular_distancia_entre_estacions(self.estacions.lista_estaciones[arribada1], self.estacions.lista_estaciones[arribada2])
        self.guanyat -= ((bicis_a_enviar_arribada1 + 9) // 10)*distancia1
        self.guanyat -= ((bicis_a_enviar_arribada2 + 9) // 10)*distancia2

    # Asegurarse de actualizar los beneficios y costos
    self.visitat[origen] = True

        
        



class Furgoneta:
    def __init__(self, origen):
        self.origen = origen
        self.destins = []  # Llista de destins
        self.bicis_per_desti = {}  # Diccionari per saber quantes bicis es deixen a cada destí
        self.capacitat = 30

        
    
