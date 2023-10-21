from copy import deepcopy
from typing import List, Generator, Set 

from bicing_estacions import *
from bicing_furgonetes import *
from bicing_parametres import *
from bicing_operators import *

class Estat(object):
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones):
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions
        
    def genera_accions_hill_climbing(self) -> Generator[Operadors, None, None]:
        
        # Set per a verificar si una estació ja ha estat assignada a una furgoneta
                
        estacions_assignades = set()
        
        for furgoneta in self.flota: 
            if furgoneta.origen is not None:
                estacions_assignades.add(furgoneta.origen)  


        
        # Per cada estació, intentar carregar bicicletes a una furgoneta
        for estacio_origen in range(len(self.estacions.lista_estaciones)):
            if estacio_origen not in estacions_assignades:  # Comprovació una furgoneta per origen
                for furgoneta in self.flota:
                    if not furgoneta.viatge_fet: #comprovació que una furgoneta sol fagi un viatge
                        for estacio_desti1 in range(len(self.estacions.lista_estaciones)):
                            if estacio_origen != estacio_desti1:
                                yield CarregarBicis(estacio_origen, estacio_desti1, None)
                                for estacio_desti2 in range(len(self.estacions.lista_estaciones)):
                                    if estacio_desti2 != estacio_origen and estacio_desti2 != estacio_desti1:
                                        yield CarregarBicis(estacio_origen, estacio_desti1, estacio_desti2)

        # Per cada furgoneta, descarrega en els seus destins
        for furgoneta in self.flota:
            if not furgoneta.viatge_fet:  # comprovació de que una furgoneta sol fagi un viatje
                if furgoneta.bicis_carregades > 0:
                    # Descarrega primer destí
                    yield DescarregarBicis(furgoneta.origen, furgoneta.primera_est, None)
                    # Si hi ha un egon destí
                    if furgoneta.segona_est is not None:
                        yield DescarregarBicis(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)


        # Per cada furgoneta amb dos destins, intentar intercanviar els destins
        for furgoneta in self.flota:
            if furgoneta.primera_est is not None and furgoneta.segona_est is not None:
                yield Intercanviar_Estacions(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)

        # Para cada furgoneta amb un segon desti, intentar eliminar-lo
        for furgoneta in self.flota:
            if furgoneta.segona_est is not None:
                yield Eliminar_Seg_Est(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)
                
        
        # Per cada furgoneta i estació, intentar canviar l'estació de origen de la furgoneta
        for furgoneta in self.flota:
            for estacio_nova in range(len(self.estacions.lista_estaciones)):
                if estacio_nova != furgoneta.origen and estacio_nova not in estacions_assignades:
                    yield Canviar_Estacio_Carr(furgoneta.origen, estacio_nova)

        # Intentar eliminar cada furgoneta
        for furgoneta in self.flota:
            if not furgoneta.viatge_fet:
                yield Esborrar_Furgoneta(furgoneta.origen)

        



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
            
            #marco el viatge com a fet
            furgoneta.viatge_fet = True 

            
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

        
    def calcular_distancia(estacio_a: Estacion, estacio_b: Estacion) -> int:
            return (abs(estacio_a.coordX - estacio_b.coordX) + abs(estacio_a.coordY - estacio_b.coordY))
    

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
        
