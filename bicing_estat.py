from copy import deepcopy
from typing import List, Generator, Set 

from bicing_estacions import *
from bicing_furgonetes import *
from bicing_parametres import *
from bicing_operators import *

class Estat(object):
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones, estacions_assignades = set()):
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions
        self.estacions_assignades = estacions_assignades
        
    def genera_accions(self):
        
        # Set per a verificar si una estació ja ha estat assignada a una furgoneta
        
        for furgoneta in self.flota: 
            if furgoneta.origen is not None:
                self.estacions_assignades.add(furgoneta.origen)  

        
        # Per cada estació, intentar carregar bicicletes a una furgoneta
        for estacio_origen in range(len(self.estacions.lista_estaciones)):
            if estacio_origen not in self.estacions_assignades:  # Comprovació una furgoneta per origen
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
                if estacio_nova != furgoneta.origen and estacio_nova not in self.estacions_assignades:
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
    
    def heurística1(self):
        ingresos = sum(furgoneta.ingresos() for furgoneta in self.flota)
        perdues = sum(furgoneta.perdues() for furgoneta in self.flota)
        return ingresos - perdues
    
    def heuristica2(self): 
        cost_gasolina = sum(furgoneta.cost_gasolina() for furgoneta in self.flota)
        ingresos = sum(furgoneta.ingresos() for furgoneta in self.flota)
        perdues = sum(furgoneta.perdues() for furgoneta in self.flota)
        return ingresos - perdues - cost_gasolina
    
    # def __repr__(self):

    # def copia(self):

    # def __eq__(self, __value):
        
