from typing import List, Generator
from copy import copy, deepcopy
from abia_bicing import Estacion, Estaciones
from bicing_furgonetes import Furgonetes, dist_estacions
from bicing_parametres import Parametres
from bicing_operators import Operadors, Intercanviar_Estacions, Eliminar_Seg_Est, Canviar_Estacio_Carr, Afegir_Furgoneta, Esborrar_Furgoneta, Carregar_Dues_Bicicletes_Més, Carregar_Dues_Bicicletes_Menys, Bici_Estacio1_A_Estacio2, Bici_Estacio2_A_Estacio1, CanviaEst1, CanviaEst2, AfegirEst1, AfegirEst2

class Estat(object):
    Contador_Estats = 0
    
    def __init__(self, parametres: Parametres,  flota: List[Furgonetes], estacions: Estaciones, estacions_origen = set()):
        Estat.Contador_Estats += 1
        self.params = parametres
        self.flota =  flota
        self.estacions = estacions
        self.estacions_origen = estacions_origen
    
    def __copy__(self):
        new_state = Estat(self.params, deepcopy(self.flota), deepcopy(self.estacions), deepcopy(self.estacions_origen))

        new_state.Contador_Estats = self.Contador_Estats

        return new_state
   
    def _repr__(self):
        return f"Estat {self.Contador_Estats} amb {len(self.flota)} furgonetes"

    
    def __eq__(self, other: "Estat") -> bool:
        #Compara si dos estats son iguals.
        if not isinstance(other, Estat):
            return False
        return (self.flota == other.flota and 
                self.estacions == other.estacions and 
                self.estacions_origen == other.estacions_origen)
    
    
    #Genera accions ha de generar totes les accions possibles a partir de l'estat actual. Utilitzant cada operador per intentar trobar una millora sobre el benefici inicial
    
    def genera_accions(self):
        
        llargada = len(self.flota) + 1
        num_max = self.params.num_furgonetes
        while llargada <= (num_max-1):
            yield Afegir_Furgoneta(self.flota, self.estacions)
            llargada = len(self.flota) + 1

        
        
        for furgoneta in self.flota:
            if furgoneta.primera_est is not None and furgoneta.segona_est is not None:
                yield Intercanviar_Estacions(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)
            if furgoneta.segona_est is not None:
                yield Eliminar_Seg_Est(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)
    
            for estacio_nova in range(len(self.estacions.lista_estaciones)):
                if estacio_nova != furgoneta.origen and estacio_nova not in self.estacions_origen:
                    yield Canviar_Estacio_Carr(furgoneta.origen, estacio_nova)
        
            yield Esborrar_Furgoneta(furgoneta.origen)
    
            estacio_origen = furgoneta.origen
            if estacio_origen is not None and furgoneta is not None and furgoneta.segona_est is not None:
                if estacio_origen.num_bicicletas_no_usadas >= 2 or (estacio_origen.num_bicicletas_no_usadas >= 1 and furgoneta.segona_est == None):
                    yield Carregar_Dues_Bicicletes_Més(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)
        
            if (furgoneta.bicis_primera >= 1 and furgoneta.bicis_segona >= 1) or (furgoneta.bicis_primera >= 1 and furgoneta.segona_est == None):
                yield Carregar_Dues_Bicicletes_Menys(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)
                
            if furgoneta.primera_est is not None and furgoneta.segona_est is not None and furgoneta.bicis_primera >= 1:
                yield Bici_Estacio1_A_Estacio2(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)
                
            if furgoneta.primera_est is not None and furgoneta.segona_est is not None and furgoneta.bicis_segona >= 1:
                yield Bici_Estacio2_A_Estacio1(furgoneta.origen, furgoneta.primera_est, furgoneta.segona_est)
        
            estacio_origen = furgoneta.origen
            estacions_ordenades = sorted(self.estacions.lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
            estacions_descarrega = [est for est in estacions_ordenades if est.num_bicicletas_next < est.demanda]
        
            for estacio_temporal in estacions_descarrega:
                if estacio_temporal != furgoneta.primera_est and estacio_temporal != furgoneta.segona_est and estacio_temporal not in self.estacions_origen:
                    if dist_estacions(estacio_origen, estacio_temporal) < dist_estacions(estacio_origen, furgoneta.primera_est):
                        yield CanviaEst1(estacio_origen, furgoneta.primera_est, furgoneta.segona_est, estacio_temporal, self.estacions.lista_estaciones)
        
            estacio_origen = furgoneta.origen
            estacions_ordenades = sorted(self.estacions.lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
            estacions_descarrega = [est for est in estacions_ordenades if est.num_bicicletas_next < est.demanda]

            for estacio_temporal in estacions_descarrega:
                if furgoneta.segona_est and estacio_temporal != furgoneta.primera_est and estacio_temporal != furgoneta.segona_est and estacio_temporal not in self.estacions_origen:
                    if dist_estacions(estacio_origen, estacio_temporal) < dist_estacions(estacio_origen, furgoneta.segona_est):
                        yield CanviaEst1(estacio_origen, furgoneta.primera_est, furgoneta.segona_est, estacio_temporal, self.estacions.lista_estaciones)

    
    def aplica_accions(self, action: Operadors):
        new_state = self.__copy__()

        def find_furgoneta_by_origen(estacio_origen):
            for furgoneta in new_state.flota:
                if furgoneta.origen == estacio_origen:
                    return furgoneta

        if isinstance(action, Intercanviar_Estacions):
            estacio_origen = action.estacio_origen 
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = find_furgoneta_by_origen(estacio_origen)

            estacio_temporal = estacio_desti
            estacio_desti = estacio_desti2
            estacio_desti2 = estacio_temporal

            if furgoneta is not None:

                furgoneta.primera_est = estacio_desti
                furgoneta.segona_est = estacio_desti2

        elif isinstance(action, Eliminar_Seg_Est):
            estacio_origen = action.estacio_origen
            estacio_desti = action.estacio_desti
            furgoneta = find_furgoneta_by_origen(estacio_origen)
            
            # Si hi ha un segon destí, reinicia les bicis i elimina el segon destí
            if furgoneta is not None and furgoneta.segona_est is not None:
                furgoneta.bicis_segona = 0
            if furgoneta is not None:
                furgoneta.segona_est = None 
        

        if isinstance(action, Afegir_Furgoneta):
            estacio_origen = estacio_desti = estacio_desti2 = None
            carrega = descarrega1 = descarrega2 = 0

            # Troba l'estació amb més bicicletes no utilitzades per posar-hi la furgoneta
            for i in self.estacions.lista_estaciones:
                if estacio_origen is None or i.num_bicicletas_no_usadas > estacio_origen.num_bicicletas_no_usadas:
                    estacio_origen = i
    
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
            furgoneta = find_furgoneta_by_origen(estacio_origen)
            
            # Si hi ha bicis carregades, les retorna a l'estació d'origen
            if furgoneta is not None:
                new_state.flota.remove(furgoneta)

        elif isinstance(action, Canviar_Estacio_Carr):
            estacio_origen_actual = action.estacio_origen_actual
            # La nova estacio origen ha de ser una estacio que no sigui origen de cap furgoneta i que tingui moltes bicis en excedent
            
            # Obté una llista de totes les estacions que no són l'origen de cap furgoneta
            estacions_candidates = [estacio for estacio in new_state.estacions.lista_estaciones if estacio not in new_state.estacions_origen]

            nova_estacio_origen = None
            max_bicicletes_en_excedent = 0

            # Troba l'estació amb la major quantitat de bicicletes en excedent
            for estacio in estacions_candidates:
                if estacio.num_bicicletas_no_usadas > max_bicicletes_en_excedent:
                    max_bicicletes_en_excedent = estacio.num_bicicletas_no_usadas
                    nova_estacio_origen = estacio

            furgoneta = find_furgoneta_by_origen(estacio_origen_actual)            
            
            # Si hi ha bicis carregades, les retorna a l'estació d'origen
            if furgoneta is not None:
                if furgoneta.bicis_carregades > 0:
                    furgoneta.bicis_carregades = 0
                    furgoneta.primera_est = None
                    furgoneta.segona_est = None
           
            # Canvia l'estació d'origen de la furgoneta
                furgoneta.origen = nova_estacio_origen
                new_state.estacions_origen.add(nova_estacio_origen)
                new_state.estacions_origen.remove(estacio_origen_actual)
        
        elif isinstance (action, Carregar_Dues_Bicicletes_Més):
            estacio_origen = action.estacio_origen
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = find_furgoneta_by_origen(estacio_origen)
            
            #Si pot carregar dos bicis més les carrega
            if estacio_origen.num_bicicletas_no_usadas >= 2 or (estacio_origen.num_bicicletas_no_usadas >= 1 and estacio_desti2 == None):
                if furgoneta is not None:
                    if estacio_desti2 is None:
                        furgoneta.bicis_primera += 1
                        furgoneta.bicis_carregades += 1
                    else:
                        furgoneta.bicis_primera += 1
                        furgoneta.bicis_segona += 1
                        furgoneta.bicis_carregades += 2
        
        elif isinstance (action, Carregar_Dues_Bicicletes_Menys):
            estacio_origen = action.estacio_origen
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = find_furgoneta_by_origen(estacio_origen)


            if furgoneta is not None:
                if (furgoneta.bicis_primera >= 1 and furgoneta.bicis_segona >= 1) or (furgoneta.bicis_primera >= 1 and estacio_desti2 == None):
                    
                    if estacio_desti2 == None:
                        furgoneta.bicis_primera -= 1
                        furgoneta.bicis_carregades -= 1
                    else:
                        furgoneta.bicis_primera -= 1
                        furgoneta.bicis_segona -= 1
                        furgoneta.bicis_carregades -= 2
            
        elif isinstance (action, Bici_Estacio1_A_Estacio2):
            estacio_origen = action.estacio_origen
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = find_furgoneta_by_origen(estacio_origen)

            #Si pot deixa una bici de les que havia de deixar a l'estació 1 a la 2
            if furgoneta is not None:
                if estacio_desti != None and estacio_desti2 != None and furgoneta.bicis_primera >= 1:
                    furgoneta.bicis_primera -= 1
                    furgoneta.bicis_segona += 1

        elif isinstance (action, Bici_Estacio2_A_Estacio1):
            estacio_origen = action.estacio_origen
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = find_furgoneta_by_origen(estacio_origen)

            #Si pot deixa una bici de les que havia de deixar a l'estació 2 a la 1
            if furgoneta is not None:
                if estacio_desti != None and estacio_desti2 != None and furgoneta.bicis_segona >= 1:
                    furgoneta.bicis_primera += 1
                    furgoneta.bicis_segona -= 1
            
            

        elif isinstance (action, CanviaEst1):
            estacio_origen = action.estacio_origen
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            furgoneta = find_furgoneta_by_origen(estacio_origen)
            estacions_ordenades = sorted(action.lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
            estacions_descarrega = [est for est in estacions_ordenades if est.num_bicicletas_next < est.demanda]
            estacio_nova = None
            
            #Canvia el primer destí on la furgoneta deixarà bicis
            if furgoneta is not None:
                for estacio_temporal in estacions_descarrega:
                    if estacio_temporal != estacio_desti and estacio_temporal != estacio_desti2 and estacio_temporal not in self.estacions_origen:
                        if estacio_nova is None or dist_estacions(estacio_origen, estacio_nova) > dist_estacions(estacio_origen, estacio_temporal):
                            estacio_nova = estacio_temporal
                
                if estacio_nova is not None:
                    furgoneta.primera_est = estacio_nova
                    estacio_desti = estacio_nova
    
            
        elif isinstance (action, CanviaEst2):
            estacio_origen = action.estacio_origen
            estacio_desti = action.estacio_desti
            estacio_desti2 = action.estacio_desti2
            
            furgoneta = find_furgoneta_by_origen(estacio_origen)
            estacions_ordenades = sorted(action.lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
            estacions_descarrega = [est for est in estacions_ordenades if est.num_bicicletas_next < est.demanda]
            estacio_nova = None

            #Canvia el segon destí on la furgoneta deixarà bicis

            if furgoneta is not None and estacio_desti2 is not None:
                for estacio_temporal in estacions_descarrega:
                    if estacio_temporal != estacio_desti and estacio_temporal != estacio_desti2 and estacio_temporal not in self.estacions_origen:
                        if estacio_nova is None or dist_estacions(estacio_origen, estacio_nova) > dist_estacions(estacio_origen, estacio_temporal):
                            estacio_nova = estacio_temporal
                
                if estacio_nova is not None:
                    furgoneta.segona_est = estacio_nova
                    estacio_desti2 = estacio_nova

        elif isinstance (action, AfegirEst1):
            estacio_origen = action.estacio_origen
            lista_estaciones = action.lista_estaciones
            furgoneta = find_furgoneta_by_origen(estacio_origen)
            estacions_ordenades = sorted(lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
            estacions_descarrega = [est for est in estacions_ordenades if est.num_bicicletas_next < est.demanda]
            estacio_nova = None

            if furgoneta is not None:
                for estacio_temporal in estacions_descarrega:
                    if estacio_desti is None and estacio_temporal != estacio_desti2 and estacio_temporal not in self.estacions_origen:
                        if estacio_nova is None or dist_estacions(estacio_origen, estacio_nova) > dist_estacions(estacio_origen, estacio_temporal):
                            estacio_nova = estacio_temporal
                
                if estacio_nova is not None:
                    furgoneta.primera_est = estacio_nova
                    if (estacio_nova.demanda > estacio_nova.num_bicicletas_no_usadas):
                        furgoneta.bicis_primera = estacio_origen.num_bicicletas_no_usadas
                        furgoneta.bicis_carregades += estacio_origen.num_bicicletas_no_usadas
                    else:
                        furgoneta.bicis_primera = estacio_nova.demanda
                        furgoneta.bicis_carregades += estacio_nova.demanda


        elif isinstance (action, AfegirEst2):
            estacio_origen = action.estacio_origen
            furgoneta = find_furgoneta_by_origen(estacio_origen)
            estacions_ordenades = sorted(action.lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
            estacions_descarrega = [est for est in estacions_ordenades if est.num_bicicletas_next < est.demanda]
            estacio_nova = None

            #Només es pot afegir segona estació si ja hi ha la primera estació

            if furgoneta is not None and furgoneta.primera_est is not None:
                for estacio_temporal in estacions_descarrega:
                    if estacio_desti is None and estacio_temporal != estacio_desti2 and estacio_temporal not in self.estacions_origen:
                        if estacio_nova is None or dist_estacions(estacio_origen, estacio_nova) > dist_estacions(estacio_origen, estacio_temporal):
                            estacio_nova = estacio_temporal
                
                if estacio_nova is not None:
                    furgoneta.segona_est = estacio_nova
                    #hem de carregar la furgoneta
                    if (estacio_nova.demanda > estacio_nova.num_bicicletas_no_usadas):
                        furgoneta.bicis_segona = estacio_origen.num_bicicletas_no_usadas
                        furgoneta.bicis_carregades += estacio_origen.num_bicicletas_no_usadas
                    else:
                        furgoneta.bicis_segona = estacio_nova.demanda
                        furgoneta.bicis_carregades += estacio_nova.demanda

        return new_state


    # Genera
    def heuristica1(self):
        ingresos = sum(furgoneta.ingresos() for furgoneta in self.flota)
        perdues = sum(furgoneta.perdues() for furgoneta in self.flota if furgoneta.perdues() is not None)
        return ingresos - perdues
    
    def heuristica2(self): 
        cost_gasolina = sum(furgoneta.cost_gasolina() for furgoneta in self.flota)
        ingresos = sum(furgoneta.ingresos() for furgoneta in self.flota)
        perdues = sum(furgoneta.perdues() for furgoneta in self.flota)
        return ingresos - perdues - cost_gasolina


# Genera un estat inicial sense furgonetes
def genera_estat_inicial_0(params: Parametres, estacions: Estaciones):
    return Estat(params, [], estacions, set())

# Genera un estat inicial on les estacions de carega i descarrega de les furgonetes es en funció de l'ordre de les estacions
def genera_estat_inicial_1(params: Parametres, estacions: Estaciones):
    def iterar_estacions(Estaciones):
        return (estacio for estacio in estacions.lista_estaciones)
    iterador_est = iterar_estacions(estacions)
    flota = []
    estacions_origen = set()
    for i in range(params.num_furgonetes):
        estacio_origen = next(iterador_est)
        estacions_origen.add(estacio_origen)
        carrega = min(estacio_origen.num_bicicletas_no_usadas, params.max_bicicletes)
        primera_est = next(iterador_est)
        bicis_primera = carrega//2
        segona_est = next(iterador_est)
        bicis_segona = carrega//2
        flota.append(Furgonetes(estacio_origen, carrega, primera_est, bicis_primera, segona_est, bicis_segona))
    return Estat(params, flota, estacions, estacions_origen)

#Genera un estat inicial que recull biciletes en les estacions amb més bicicletes_no_usades i les porta a les estacions amb demanda més properes
def genera_estat_inicial_2(params: Parametres, estacions: Estaciones):
    flota = []
    estacions_ordenades = sorted(estacions.lista_estaciones, key=lambda est: est.num_bicicletas_next - est.demanda, reverse=True)
    estacions_excedent = [est for est in estacions_ordenades if est.num_bicicletas_next > est.demanda]
    estacions_carrega = estacions_excedent[0:params.num_furgonetes]
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
