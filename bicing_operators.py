
from bicing_furgonetes import Furgonetes
from bicing_estacions import Estacion

class Operadors:
    pass

class CarregarBicis(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2

    def __repr__(self) -> str:
        return f"Carrega bicis a la furgoneta de l'estació {self.estacio_origen}"



class DescarregarBicis(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
            
    def __repr__(self) -> str:
        if self.estacio_desti2:
            return f"Descarrega bicis a l'estació {self.estacio_desti} i {self.estacio_desti2}"
        else:
            return f"Descarrega bicis a l'estació {self.estacio_desti}"

        

                
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
            
        return guanys_totals

        
        
            

class Intercanviar_Estacions(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
            self.estacio_origen = estacio_origen
            self.estacio_desti = estacio_desti
            self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str:
            return f"Intercanvia el recorregut de les estacions, primer es va a {self.estacio_desti2} i després a {self.estacio_desti}"
        



#Nou operador: eliminar segona estació de descàrrega
class Eliminar_Seg_Est(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str:
        return f"Elimina la segona estació ({self.estacio_desti2} de la ruta."


class Canviar_Estacio_Carr(Operadors):
    def __init__(self, estacio_origen_actual: Estacion, nova_estacio_origen: Estacion):
        self.estacio_origen_actual = estacio_origen_actual
        self.nova_estacio_origen = nova_estacio_origen

    def __repr__(self) -> str:
        return f"Canvia l'estació d'origen de la furgoneta de {self.estacio_origen_actual} a {self.nova_estacio_origen}"

    def executa(self, estacions, flota):
        #EI! NO ESTIC SEGUR DE QUE AQUEST FOR SIGUI NECESSARI O SI JA TENIM LA FURGONETA SELECCIONADA
        #EN CAS DE QUE SIGUI AIXÍ, ES POT ESBORRAR
            
        for furgoneta in flota: 
            if furgoneta.origen == self.estacio_origen_actual:
                # Comprova si la furgoneta està carregada, per si ho està descarregar-la
                if furgoneta.bicis_carregades > 0:
                    estacions.lista_estaciones[self.estacio_origen_actual].num_bicicletas_next += furgoneta.bicis_carregades 
                    furgoneta.bicis_carregades = furgoneta.bicis_primera = furgoneta.bicis_segona = 0
                    furgoneta.primera_est = furgoneta.segona_est = None
                    
                # Canvia l'estació d'origen de la furgoneta
                furgoneta.origen = self.nova_estacio_origen

                # Haurem de carregar la furgoneta novament però això no es fa en aquesta funció 
                # sinó que després d'aquesta fucnió sempre es pot cridar a carregar un altre cop
                break


class Esborrar_Furgoneta(Operadors):
    def __init__(self, estacio_origen: Estacion):
        self.estacio_origen = estacio_origen

    def __repr__(self) -> str:
        return f"Suprimeix la furgoneta amb estació d'origen {self.estacio_origen}"
