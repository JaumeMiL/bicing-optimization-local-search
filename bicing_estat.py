from copy import deepcopy
from typing import List, Generator, Set 

from bicing_estacions import *
from bicing_furgonetes import *
from bicing_parametres import *
from distancia_estacions import calcular_distancia

class Estat(object):
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones):
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions
    from bicing_operators import CarregarBicis, DescarergarBicis, Intercanviar_Estacions, Calcular_Guanys
from bicing_estacions import Estacions
from bicing_furgonetes import Furgonetes

class BicingState:
    def __init__(self, estacions: Estacions, furgonetes: Furgonetes):
        self.estacions = estacions
        self.furgonetes = furgonetes

    def generate_actions(self):
        # The list to store potential actions
        potential_actions = []

        # We'll limit the actions based on available vans and stations
        # For simplicity, we'll generate actions for each combination of van and station.
        for furgoneta_id, furgoneta in enumerate(self.furgonetes):
            for estacio_id, estacio in enumerate(self.estacions.lista_estaciones):
                # Ensure we're not loading from a station we've already visited
                if estacio_id not in furgoneta.origens:
                    # Generate CarregarBicis actions
                    for desti_id, estacio_desti in enumerate(self.estacions.lista_estaciones):
                        if estacio_id != desti_id:  # Ensure origin and destination are not the same
                            action = CarregarBicis(furgoneta_id, estacio_id, desti_id)
                            potential_actions.append(action)

                    # Generate DescarergarBicis actions
                    for desti_id, estacio_desti in enumerate(self.estacions.lista_estaciones):
                        if estacio_id != desti_id:  # Ensure origin and destination are not the same
                            action = DescarergarBicis(furgoneta_id, estacio_id, desti_id)
                            potential_actions.append(action)

                    # Generate Intercanviar_Estacions actions only if there's a second destination already specified
                    if furgoneta.destins:
                        for desti_id, estacio_desti in enumerate(self.estacions.lista_estaciones):
                            if estacio_id != desti_id:  # Ensure origin and destination are not the same
                                action = Intercanviar_Estacions(furgoneta_id, estacio_id, desti_id)
                                potential_actions.append(action)

        # Generate Calcular_Guanys actions for every pair of stations
        for estacio_id, estacio in enumerate(self.estacions.lista_estaciones):
            for desti_id, estacio_desti in enumerate(self.estacions.lista_estaciones):
                if estacio_id != desti_id:  # Ensure origin and destination are not the same
                    action = Calcular_Guanys(estacio_id, desti_id)
                    potential_actions.append(action)

        return potential_actions
    
    
    def apply_action(self, action):
        # Crear una copia profunda del estado para no modificar el estado original
        new_estacions = copy.deepcopy(self.estacions)
        new_furgonetes = copy.deepcopy(self.furgonetes)
        
        # Aplicar la acción en las copias
        if isinstance(action, CarregarBicis):
            action.executa(new_estacions, new_furgonetes)
        elif isinstance(action, DescarregarBicis):
            action.executa(new_estacions, new_furgonetes)
        elif isinstance(action, Intercanviar_Estacions):
            action.executa()
        
        # Devolver el nuevo estado
        return BicingState(new_estacions, new_furgonetes)
# Test:
# estacions = ...  # Load Estacions instance
# furgonetes = ...  # Load Furgonetes instance
# state = BicingState(estacions, furgonetes)
# actions = state.generate_actions()

    #Copia

    #Repr

    #Genera Accions

    #Aplica accions

    #Heurística

class Estat:
    def __init__(self, num_estacions, num_bicis, semilla, num_furgos):
        self.estacions = Estaciones(num_estacions, num_bicis, semilla)
        self.visitat = [False] * num_estacions
        self.furgonetes = [Furgonetes(i) for i in range(1, num_furgos+1)]
        self.guanyat = 0
    


def apply_action(self, action: Operadors) -> StateRepresentation:
    if isinstance(action,Carregar_bicis):
        Carregar_bicis.execut

        
        



