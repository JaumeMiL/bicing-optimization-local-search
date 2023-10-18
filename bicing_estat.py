import random
import math
import copy
from copy import deepcopy
from typing import List, Set, Generator

from bicing_estacions import Estacion, Estaciones
from bicing_parametres import Parametres
from bicing_furgonetes import Furgonetes
from bicing_operators import *

class Estat(object):
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones, estacions_origen: set() = None):
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions
        self.estacions_origen = estacions_origen

    def copy(self) -> Estat:
        return Estat(self.params, self.estacions.copy(), self.flota.copy(), self.estacions_origen.copy())

    def __repr__(self) -> str:
        return f"estacions={str(self.estacions)} | flota={self.flota} | {self.params}"

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
    
    def heuristica:
    """
    class Calcular_Guanys(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str:
        if self.estacio_desti2:
            return f"Calcular costos desde l'estació {self.estacio_origen} fins {self.estacio_desti}"
        else:   
            return f"Calcular costos desde l'estació {self.estacio_origen} fins {self.estacio_desti} i {self.estacio_desti2}"

    def executa(self, estacions, furgonetes):
        furgoneta = furgonetes[self.estacio_origen]
        bicis_a_enviar_desti1, bicis_a_enviar_desti2 = self.calcular_bicis_a_enviar(furgoneta, estacions, self.estacio_origen, self.estacio_desti, self.estacio_desti2)
        
        # Costos per distancia
        distancia1 = self.calcular_distancia(estacions, self.estacio_origen, self.estacio_desti)/1000
        cost_distancia1 = -((bicis_a_enviar_desti1 + 9) // 10) * distancia1
        
        # Si hi ha segon destí
        if self.estacio_desti2:
            distancia2 = self.calcular_distancia(estacions, self.estacio_desti, self.estacio_desti2)/1000
            cost_distancia2 = -((bicis_a_enviar_desti2 + 9) // 10) * distancia2 
        else:
            cost_distancia2 = 0
        
        # Benefici per apropar bicis a la demanda
        estacio_desti_obj = estacions.lista_estaciones[self.estacio_desti]
        benefici_desti = max(0, estacio_desti_obj.demanda - estacio_desti_obj.num_bicicletas_next)
        
        # Si hi ha segon destí
        if self.estacio_desti2:
            estacio_desti2_obj = estacions.lista_estaciones[self.estacio_desti2]
            benefici_desti2 = max(0, estacio_desti2_obj.demanda - estacio_desti2_obj.num_bicicletas_next)
        else:
            benefici_desti2 = 0
            
        # Costos per apropar bicis a la demanda
        estacio_desti_obj = estacions.lista_estaciones[self.estacio_desti]
        cost_desti = min(0, estacio_desti_obj.demanda - estacio_desti_obj.num_bicicletas_next)
        
        # Si hi ha segon destí
        if self.estacio_desti2:
            estacio_desti2_obj = estacions.lista_estaciones[self.estacio_desti2]
            benefici_desti2 = min(0, estacio_desti2_obj.demanda - estacio_desti2_obj.num_bicicletas_next)
        else:
            cost_desti2 = 0
            
        
        
        #Guanys totals
        guanys_totals = cost_distancia1 + cost_distancia2 + benefici_desti + benefici_desti2 + cost_desti + cost_desti2
        
        return guanys_totals"""

def generate_initial_state(params: ProblemParameters) -> StateRepresentation:
    assert (params.p_max <= params.c_max)

    v_p = [c_i for c_i in range(params.c_max)]
    return StateRepresentation(params, v_p)

def generate_initial_state_greedy(params: Parametres) -> Estat:
    assert (params.p_max <= params.c_max)
    c_i = 0
    h_c_i = params.h_max
    v_p = []
    for p_i in range(params.p_max):
        h_p_i = params.v_h[p_i]
        if h_p_i > h_c_i:  # Paquet no cap en contenidor c_i
            c_i = c_i + 1  # Contenidor nou
            h_c_i = params.h_max - h_p_i
        else:
            h_c_i = h_c_i - h_p_i
        v_p.append(c_i)
    return StateRepresentation(params, v_p)
