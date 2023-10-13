import random
from abia_bicing import *
class Estat:
    def __init__(self, num_estacions, num_bicis, semilla, num_furgos):
        self.estacions = Estaciones(numestacions, num_bicis, semilla)
        self.visitat = [False] * num_estacions
        self.furgonetes = [Furgoneta(i) for i in range(1, num_furgos+1)]
        self.costos = 0
        self.beneficis = 0
        
    def moure_bicis(self,origen,arribada1,arribada2):
        furgoneta = self.furgonetes[origen]
        #hauriem de tenir alguna forma d'identificar les estacions
        
        


class Furgoneta:
    
    def __init__(self,origen):
        self.origen = origen
        self.capacitat = 30
        
    def set_origen(self,origen1):
        self.origen = origen1
        
    def get_origen(self):
        return self.origen
    
