from copy import deepcopy
from typing import List, Generator, Set 

from abia_bicing import Estacion, Estaciones
from bicing_furgonetes import Furgonetes, dist_estacions
from bicing_parametres import Parametres
from bicing_operators import *
from bicing_operators import Operadors
from bicing_estat import Estat




class Estat(object):
    
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones, estacions_origen = set()):
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions
        self.estacions_origen = estacions_origen
        

    def copy(self) -> Estat:
        flota_copy = deepcopy(self.flota)
        estacions_copy = deepcopy(self.estacions)
        estacions_origen_copy = deepcopy(self.estacions_origen)
        
        return Estat(self.params, flota_copy, estacions_copy, estacions_origen_copy)
    
    def __repr__(self) -> str:

        return f"Estat(Flota: {self.flota}, Estaciones: {len(self.estacions.lista_estaciones)}, Estaciones Origen: {self.estacions_origen})"
    
    
    def __eq__(self, other: "Estat") -> bool:
        
        #Compara si dos estats son iguals.
        if not isinstance(other, Estat):
            return False
        return (self.flota == other.flota and 
                self.estacions == other.estacions and 
                self.estacions_origen == other.estacions_origen)

        
    def aplica_accions(self, action: Operadors) -> Estat:
        new_state = self.copy()
        
        if isinstance(action, DescarregarBicis):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = new_state.flota[estacio_origen]
            
            # Calcula les bicis a enviar a cada destinació
            demanda_desti = new_state.estacions.lista_estaciones[estacio_desti].demanda
            bicis_a_enviar = min(furgoneta.capacitat, new_state.estacions.lista_estaciones[estacio_origen].num_bicicletas_next, demanda_desti)
            bicis_a_enviar_desti1 = bicis_a_enviar

            bicis_a_enviar_desti2 = 0
            if estacio_desti2 is not None:
                demanda_desti2 = new_state.estacions.lista_estaciones[estacio_desti2].demanda
                bicis_a_enviar_desti2 = min(furgoneta.capacitat - bicis_a_enviar_desti1, demanda_desti2)
                bicis_a_enviar += bicis_a_enviar_desti2

            # Descarrega bicis al destí 1
            new_state.estacions.lista_estaciones[estacio_desti].num_bicicletas_no_usadas += bicis_a_enviar_desti1

            # Descarrega bicis al destí 2 si existeix
            if estacio_desti2:
                new_state.estacions.lista_estaciones[estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2

            # Actualitza la furgoneta i les estacions destí
            furgoneta.primera_est = estacio_desti
            furgoneta.bicis_primera = bicis_a_enviar_desti1
            new_state.estacions.lista_estaciones[estacio_desti].num_bicicletas_no_usadas += bicis_a_enviar_desti1

            if estacio_desti2:
                furgoneta.segona_est = estacio_desti2
                furgoneta.bicis_segona = bicis_a_enviar_desti2
                new_state.estacions.lista_estaciones[estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2

            # Marca el viatge com a realitzat
            furgoneta.viatge_fet = True 

        elif isinstance(action, Intercanviar_Estacions):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = new_state.flota[estacio_origen]
            
            # Assegura't que hi ha un segon destí
            assert estacio_desti2 is not None
            estacio_desti, estacio_desti2 = estacio_desti2, estacio_desti

        elif isinstance(action, Eliminar_Seg_Est):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            furgoneta = new_state.flota[estacio_origen]
            
            # Si hi ha un segon destí, reinicia les bicis i elimina el segon destí
            if furgoneta.segona_est is not None:
                var_temp_bicis_desti2 = furgoneta.bicis_segona
                furgoneta.bicis_segona = 0
                new_state.estacions.lista_estaciones[estacio_desti].num_bicicletas_next += var_temp_bicis_desti2
            furgoneta.segona_est = None

        elif isinstance(action, Afegir_Furgoneta):
            if len(action.flota) < self.params.n_furgonetes:
                estacio_origen = estacio_desti = estacio_desti2 = None
                carrega = descarrega1 = descarrega2 = 0

                # Troba l'estació amb més bicicletes no utilitzades per posar-hi la furgoneta
                for i in self.estacions.lista_estaciones:
                    if estacio_origen is None or i.num_bicicletas_no_usadas > estacio_origen.num_bicicletas_no_usadas:
                        estacio_origen = i
                        variable_temp_no_usades = i.num_bicicletas_no_usadas #necesito saber quantes bicis no usades hi ha

                if estacio_origen is not None:
                    # Busca la primera estació per descarregar més propera
                    distancia_minima, estacio_desti = float('inf'), None
                    for est in action.estacions.lista_estaciones:
                        if est.num_bicicletas_next - est.demanda < 0 and est is not estacio_origen:
                            distancia = dist_estacions(estacio_origen, est)
                            if distancia < distancia_minima:
                                distancia_minima = distancia
                                estacio_desti = est

                    if estacio_desti is not None:
                        # Calcula la quantitat de bicicletes a descarregar a la primera estació de descàrrega
                        if (estacio_desti.num_bicicletas_next - estacio_desti.demanda < 0):
                            if (estacio_origen.num_bicicletas_no_usadas > abs(estacio_desti.num_bicicletas_next - estacio_desti.demanda)):
                                descarrega1 = abs(estacio_desti.num_bicicletas_next - estacio_desti.demanda)
                            else:
                                descarrega1 = estacio_origen.num_bicicletas_no_usadas
                        
                        carrega += descarrega1
                        estacio_origen.num_bicicletas_no_usadas -= descarrega1

                        if estacio_origen.num_bicicletas_no_usadas != 0:
                            # Busca l'estació de descàrrega més propera per a la segona estació
                            distancia_minima2, est_descarrega_propera2 = float('inf'), None
                            for est_des in action.estacions.lista_estaciones:
                                if (est_des.num_bicicletas_next - est_des.demanda < 0) and est_des is not estacio_desti and est_des is not estacio_origen:
                                    distancia = dist_estacions(estacio_desti, est_des)
                                    if distancia < distancia_minima2:
                                        distancia_minima2 = distancia
                                        estacio_desti2 = est_des

                            if estacio_desti2 is not None:
                                # Calcula la quantitat de bicicletes a descarregar a la segona estació
                                if (estacio_desti.num_bicicletas_next - estacio_desti.demanda < 0):
                                    if (estacio_origen.num_bicicletas_no_usadas > abs(estacio_desti.num_bicicletas_next - estacio_desti.demanda)):
                                        descarrega2 = abs(estacio_desti.num_bicicletas_next - estacio_desti.demanda)
                                    else:
                                        descarrega2 = estacio_origen.num_bicicletas_no_usadas

                            carrega += descarrega2
                            estacio_origen.num_bicicletas_no_usadas -= descarrega2
                            
                # Crea una nova furgoneta amb l'estació d'origen, la càrrega i les estacions de descàrrega
                nova_furgo = Furgonetes(estacio_origen, carrega, estacio_desti, descarrega1, estacio_desti2, descarrega2)

                # Afegix la nova furgoneta a la flota
                action.flota.append(nova_furgo)


        elif isinstance(action, Esborrar_Furgoneta):
            estacio_origen = action.estacio_origen 
            furgoneta = new_state.flota[estacio_origen]
            
            # Si hi ha bicis carregades, les retorna a l'estació d'origen
            if furgoneta.bicis_carregades > 0:
                new_state.estacions.lista_estaciones[estacio_origen].num_bicicletas_next += furgoneta.bicis_carregades 
                furgoneta.bicis_carregades = 0
                furgoneta.primera_est = None
                furgoneta.segona_est = None
            new_state.flota.remove(furgoneta)

        elif isinstance(action, Canviar_Estacio_Carr):
            estacio_origen_actual = action.estacio_origen_actual
            nova_estacio_origen = action.nova_estacio
            furgoneta = new_state.flota[estacio_origen_actual]
            
            # Si hi ha bicis carregades, les retorna a l'estació d'origen
            if furgoneta.bicis_carregades > 0:
                new_state.estacions.lista_estaciones[estacio_origen_actual].num_bicicletas_next += furgoneta.bicis_carregades 
                furgoneta.bicis_carregades = 0
                furgoneta.primera_est = None
                furgoneta.segona_est = None

            # Canvia l'estació d'origen de la furgoneta
            furgoneta.origen = nova_estacio_origen

        return new_state


    
    def heuristica1(self):
        ingresos = sum(furgoneta.ingresos() for furgoneta in self.flota)
        perdues = sum(furgoneta.perdues() for furgoneta in self.flota)
        return ingresos - perdues
    
    def heuristica2(self): 
        cost_gasolina = sum(furgoneta.cost_gasolina() for furgoneta in self.flota)
        ingresos = sum(furgoneta.ingresos() for furgoneta in self.flota)
        perdues = sum(furgoneta.perdues() for furgoneta in self.flota)
        return ingresos - perdues - cost_gasolina


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
