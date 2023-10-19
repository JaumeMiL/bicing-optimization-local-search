import random

from bicing_estacions import *
from bicing_estat import *


class Furgonetes(object):

    def __init__(self, origen: Estacion, bicis_carregades: int = 0, primera_est: Estacion = None, bicis_primera: int = 0, segona_est: Estacion = None, bicis_segona: int = 0):
        self.origen = origen  # Estació on carrega
        self.primera_est = primera_est  # Primera estació
        self.segona_est = segona_est  # Segona estació
        self.bicis_carregades = bicis_carregades  
        self.bicis_primera = bicis_primera  # Nombre de bicis que es deixen a la primera estació
        self.bicis_segona = bicis_segona  # Nombre de bicis que es deixen a la segona estació
        self.capacitat = 30 #Capacitat màxima de la furgoneta
        self.viatge_fet = False #Marca si ha fet el viatge

        if primera_est is None:
            assert bicis_primera == 0  # Si no hi ha primera estació, la quantitat de bicis ha de ser 0

        if segona_est is None:
            assert bicis_segona == 0  # Si no hi ha segona estació, la quantitat de bicis ha de ser 0




