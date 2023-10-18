from copy import deepcopy
from typing import List, Generator, Set 

from bicing_estacions import *
from bicing_furgonetes import *
from bicing_parametres import *
from distancia_estacions import calcular_distancia
from bicing_operators import *

class Estat(object):
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones):
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions


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
    
    #@staticmethod
    #def calcular_bicis_a_enviar(furgoneta, estacions, estacio_origen, estacio_desti, estacio_desti2=None):
    #    demanda_desti = estacions.lista_estaciones[estacio_desti].demanda
    #    bicis_a_enviar = min(furgoneta.capacitat, estacions.lista_estaciones[estacio_origen].num_bicicletas_next, demanda_desti)
    #    bicis_a_enviar_desti1 = bicis_a_enviar
    #    
    #    bicis_a_enviar_desti2 = 0
    #    if estacio_desti2 is not None:
    #        demanda_desti2 = estacions.lista_estaciones[estacio_desti2].demanda
    #        bicis_a_enviar_desti2 = min(furgoneta.capacitat - bicis_a_enviar_desti1, demanda_desti2)
    #        bicis_a_enviar += bicis_a_enviar_desti2
        
    #    return bicis_a_enviar_desti1, bicis_a_enviar_desti2
    
    #@staticmethod
    #def calcular_distancia(estacio_a: Estacion, estacio_b: Estacion) -> int:
    #   return (abs(estacio_a.coordX - estacio_b.coordX) + abs(estacio_a.coordY - estacio_b.coordY)) 
    
    def apply_action(self, action: Operadors):
        new_estacions = copy.deepcopy(self.estacions)
        new_flota = copy.deepcopy(self.flota) 
        
        
        if isinstance(action, CarregarBicis):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti
            furgoneta = new_flota[estacio_origen]
            
            
            demanda_desti = new_estacions.lista_estaciones[estacio_desti].demanda
            bicis_a_enviar = min(furgoneta.capacitat, new_estacions.lista_estaciones[estacio_origen].num_bicicletas_next, demanda_desti)
            bicis_a_enviar_desti1 = bicis_a_enviar
        
            bicis_a_enviar_desti2 = 0
            if estacio_desti2 is not None:
                demanda_desti2 = new_estacions.lista_estaciones[estacio_desti2].demanda
                bicis_a_enviar_desti2 = min(furgoneta.capacitat - bicis_a_enviar_desti1, demanda_desti2)
                bicis_a_enviar += bicis_a_enviar_desti2
            
        
            
            # Actualitzar la furgoneta i l'estació d'origen en cas que no hi hagi segona estació
            furgoneta.bicis_carregades += (bicis_a_enviar_desti1 + bicis_a_enviar_desti2)
            furgoneta.origen = estacio_origen
            new_estacions.lista_estaciones[estacio_origen].num_bicicletas_next -= bicis_a_enviar_desti1
        
            #Actualitzar l'estacó d'origen en el cas de que si que n'hi hagi
            if estacio_desti2:
                new_estacions.lista_estaciones[estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2
        
            #S'HA DE mARCAR Q JA S'HA SORTIT D'AQUEST ORIGEN I COMPROVAR QUAN ES GENERIN ACCIONS CREC
            
            
        elif isinstance(action, DescarregarBicis):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti
            furgoneta = new_flota[estacio_origen]
            
            #calcular les bicis a enviar a cada destí
            demanda_desti = new_estacions.lista_estaciones[estacio_desti].demanda
            bicis_a_enviar = min(furgoneta.capacitat, new_estacions.lista_estaciones[estacio_origen].num_bicicletas_next, demanda_desti)
            bicis_a_enviar_desti1 = bicis_a_enviar
        
            bicis_a_enviar_desti2 = 0
            if estacio_desti2 is not None:
                demanda_desti2 = new_estacions.lista_estaciones[estacio_desti2].demanda
                bicis_a_enviar_desti2 = min(furgoneta.capacitat - bicis_a_enviar_desti1, demanda_desti2)
                bicis_a_enviar += bicis_a_enviar_desti2
            
            #Descarregar bicis destí 1
            new_estacions.lista_estaciones[estacio_desti].num_bicicletas_no_usadas += bicis_a_enviar_desti1
        
            #Descarregar bicis destí 2 si n'hi ha
            if estacio_desti2:
                new_estacions.lista_estaciones[estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2

            #Actualitzar la furgoneta i les estacions destí
            furgoneta.primera_est = estacio_desti
            furgoneta.bicis_primera = bicis_a_enviar_desti1
            new_estacions.lista_estaciones[estacio_desti].num_bicicletas_no_usadas += bicis_a_enviar_desti1
        
            if estacio_desti2:
                furgoneta.segona_est = estacio_desti2
                furgoneta.bicis_segona = bicis_a_enviar_desti2
                new_estacions.lista_estaciones[estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2

            
        elif isinstance(action, Intercanviar_Estacions):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti
            furgoneta = new_flota[estacio_origen]
            
            assert estacio_desti2 is not None
            estacio_desti, estacio_desti2 = estacio_desti2, estacio_desti
        
        elif isinstance(action,Eliminar_Seg_Est):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti
            furgoneta = new_flota[estacio_origen]
            
            if furgoneta.segona_est is not None:
                
                var_temp_bicis_desti2 = furgoneta.bicis_segona
                furgoneta.bicis_segona = 0 #reinicio a 0 les que havia d'enviar
                #les bicis que hi haurà a l'est_origen seran les que ja havia agafat
                new_estacions.lista_estaciones[estacio_desti2].num_bicicletas_next += var_temp_bicis_desti2
            estacio_desti2 = None
            
        elif isinstance(action,Esborrar_Furgoneta):
            estacio_origen = action.estacio_origen 
            furgoneta = new_flota[estacio_origen]
            
            if furgoneta.bicis_carregades > 0:
                    new_estacions.lista_estaciones[estacio_origen].num_bicicletas_next += furgoneta.bicis_carregades 
                    furgoneta.bicis_carregades = furgoneta.bicis_primera = furgoneta.bicis_segona = 0
                    furgoneta.primera_est = furgoneta.segona_est = None
            new_flota.remove(furgoneta)  # Elimina la furgoneta de la llista de furgonetes
        
        elif isinstance(action,Canviar_Estacio_Carr):
            estacio_origen_actual = action.estacio_origen_actual
            nova_estacio_origen = action.nova_estacio
            furgoneta = new_flota[estacio_origen_actual]
            
            if furgoneta.bicis_carregades > 0:
                    new_estacions.lista_estaciones[estacio_origen_actual].num_bicicletas_next += furgoneta.bicis_carregades 
                    furgoneta.bicis_carregades = furgoneta.bicis_primera = furgoneta.bicis_segona = 0
                    furgoneta.primera_est = furgoneta.segona_est = None
                    
            # Canvia l'estació d'origen de la furgoneta
            furgoneta.origen = nova_estacio_origen
            
        
       
        return new_estacions, new_flota
# Test:
# estacions = ...  # Load Estacions instance
# furgonetes = ...  # Load Furgonetes instance
# state = BicingState(estacions, furgonetes)
# actions = state.generate_actions()

    #Copia

    #Repr

    #Genera Accions

    #Aplica accions

    #Heurística Podem utilitzar les que tenim ja creades en l'operador o mirar de fer que ho calculi tot arribat a l'estat fina

        
    
    

    def heuristica1(self):

        for furgoneta in self.flota:
            
        
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
            
            return guanys_totals
