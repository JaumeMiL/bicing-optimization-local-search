from copy import deepcopy
from typing import List, Generator, Set 

from bicing_estacions import Estacion, Estaciones
from bicing_furgonetes import Furgonetes, dist_estacions
from bicing_parametres import Parametres
from bicing_operators import *

class Estat(object):
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones, estacions_origen = set()):
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions
        self.estacions_origen = estacions_origen
        
    def genera_accions(self):
        
        # Set per a verificar si una estació ja ha estat assignada a una furgoneta
        
        for furgoneta in self.flota: 
            if furgoneta.origen is not None:
                self.estacions_origen.add(furgoneta.origen)  

        
        # Per cada estació, intentar carregar bicicletes a una furgoneta
        for estacio_origen in range(len(self.estacions.lista_estaciones)):
            if estacio_origen not in self.estacions_origen:  # Comprovació una furgoneta per origen
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
                if estacio_nova != furgoneta.origen and estacio_nova not in self.estacions_origen:
                    yield Canviar_Estacio_Carr(furgoneta.origen, estacio_nova)

        # Intentar eliminar cada furgoneta
        for furgoneta in self.flota:
            if not furgoneta.viatge_fet:
                yield Esborrar_Furgoneta(furgoneta.origen)


    def aplica_accions(self, action: Operadors):
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
    
    def heuristica1(self):
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

# Funcions de generació dels diferents estats inicials

# Genera un estat inicial sense furgonetes
def genera_estat_inicial_0(params: Parametres, estacions: Estaciones) -> Estat:
    return Estat(params, [], estacions, set())

# Genera un estat inicial on les estacions de carega i descarrega de les furgonetes es en funció de l'ordre de les estacions
def genera_estat_inicial_1(params: Parametres, estacions: Estaciones) -> Estat:
    def iterar_estacions(Estaciones) -> Generator[Estacion, None, None]:
        return (estacio for estacio in estacions.lista_estaciones)
    iterador_est = iterar_estacions(estacions)
    flota = []
    estacions_origen = set()
    for i in range(params.n_furgonetes):
        estacio_origen = next(iterador_est)
        estacions_origen.add(estacio_origen)
        carrega = estacio_origen.num_bicicletas_no_usadas
        primera_est = next(iterador_est)
        bicis_primera = carrega
        flota.append(Furgonetes(estacio_origen, carrega))
    return Estat(params, flota, estacions, estacions_origen)

#Genera un estat inicial que recull biciletes en les estacions amb més bicicletes_no_usades i les porta a les estacions amb demanda més properes
def genera_estat_inicial_2(params: Parametres, estacions: Estaciones) -> Estat:
    flota = []
    estacions_ordenades = sorted(estacions.lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
    estacions_excedent = [est for est in estacions_ordenades if est.num_bicicletas_next > est.demanda]
    estacions_carrega = estacions_excedent[0:params.n_furgonetes]
    estacions_descarrega = [est for est in estacions_ordenades if est.num_bicicletas_next < est.demanda]
    
    for est_carrega in estacions_carrega:
        distancia_minima = float('inf')
        est_descarrega_propera = None
        distancia_minima2 = float('inf')
        est_2descarrega_propera = None
        carrega_max = min(est_carrega.num_bicicletas_no_usadas, (est_carrega.num_bicicletas_next-est_carrega.demanda), params.max_bicicletes)

        for est_descarrega in estacions_descarrega:
            distancia = dist_estacions(est_carrega, est_descarrega)
            if distancia < distancia_minima:
                distancia_minima, est_descarrega_propera = distancia, est_descarrega
        
        descarrega = min(est_descarrega_propera.demanda - est_descarrega_propera.num_bicicletas_next, carrega_max)
        
        if (est_descarrega_propera.demanda - est_descarrega_propera.num_bicicletas_next) == 0:
            estacions_descarrega.remove(est_descarrega_propera) 

        for est_descarrega2 in estacions_descarrega: 
            distancia2 = dist_estacions(est_descarrega_propera, est_descarrega2)
            if distancia2 < distancia_minima2:
                distancia_minima2, est_2descarrega_propera = distancia2, est_descarrega2
        
        descarrega2 = min((carrega_max - descarrega),(est_2descarrega_propera.demanda - est_2descarrega_propera.num_bicicletas_next))
        
        if (est_2descarrega_propera.demanda - est_2descarrega_propera.num_bicicletas_next) == 0:
            estacions_descarrega.remove(est_2descarrega_propera)

        carrega = min(carrega_max, (descarrega + descarrega2))        
        
        flota.append(Furgonetes(est_carrega, carrega, est_descarrega_propera, descarrega, est_2descarrega_propera, descarrega2))
    
    return Estat(params, flota, estacions, set(estacions_carrega))
