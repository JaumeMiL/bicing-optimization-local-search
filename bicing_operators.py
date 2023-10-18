
from bicing_furgonetes import Furgonetes
from bicing_estacions import Estacion

class Operadors:
    estaciones_visitades = set()
    
    @staticmethod
    def calcular_bicis_a_enviar(furgoneta, estacions, estacio_origen, estacio_desti, estacio_desti2=None):
        demanda_desti = estacions.lista_estaciones[estacio_desti].demanda
        bicis_a_enviar = min(furgoneta.capacitat, estacions.lista_estaciones[estacio_origen].num_bicicletas_next, demanda_desti)
        bicis_a_enviar_desti1 = bicis_a_enviar
        
        bicis_a_enviar_desti2 = 0
        if estacio_desti2 is not None:
            demanda_desti2 = estacions.lista_estaciones[estacio_desti2].demanda
            bicis_a_enviar_desti2 = min(furgoneta.capacitat - bicis_a_enviar_desti1, demanda_desti2)
            bicis_a_enviar += bicis_a_enviar_desti2
        
        return bicis_a_enviar_desti1, bicis_a_enviar_desti2
    
    @staticmethod
    def calcular_distancia(estacio_a: Estacion, estacio_b: Estacion) -> int:
        return (abs(estacio_a.coordX - estacio_b.coordX) + abs(estacio_a.coordY - estacio_b.coordY))


class CarregarBicis(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2

    def __repr__(self) -> str:
        return f"Carrega bicis a la furgoneta de l'estació {self.estacio_origen}"

    def executa(self, estacions, furgonetes):
        furgoneta = furgonetes[self.estacio_origen]
        
        bicis_a_enviar_desti1, bicis_a_enviar_desti2 = self._calcular_bicis_a_enviar(furgoneta, estacions, self.estacio_origen, self.estacio_desti, self.estacio_desti2)
        
        # Actualitzar la furgoneta i l'estació d'origen en cas que no hi hagi segona estació
        furgoneta.capacitat -= (bicis_a_enviar_desti1 + bicis_a_enviar_desti2)
        estacions.lista_estaciones[self.estacio_origen].num_bicicletas_next -= bicis_a_enviar_desti1
        
        #Actualitzar l'estacó d'origen en el cas de que si que n'hi hagi
        if self.estacio_desti2:
            estacions.lista_estaciones[self.estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2
        
        #Es marca que ja s'ha sortit des d'aquesta estació S'HA DE COMPROVAR QUAN ES GENERIN ACCIONS CREC
        Operadors.estacions_visitades.add(self.estacio_origen)

class DescarergarBicis(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str:
        if self.estacio_desti2:
            return f"Descarrega bicis a l'estació {self.estacio_desti} i {self.estacio_desti2}"
        else:
            return f"Descarrega bicis a l'estació {self.estacio_desti}"

    def executa(self, estacions, furgonetes):
        
        furgoneta = furgonetes[self.estacio_origen]
        
        bicis_a_enviar_desti1, bicis_a_enviar_desti2 = self.calcular_bicis_a_enviar(furgoneta, estacions, self.estacio_origen, self.estacio_desti, self.estacio_desti2)
        
        #Descarregar bicis destí 1
        estacions.lista_estaciones[self.estacio_desti].num_bicicletas_no_usadas += bicis_a_enviar_desti1
        
        #Descarregar bicis destí 2 si n'hi ha
        if self.estacio_desti2:
            estacions.lista_estaciones[self.estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2

        #Actualitzar la furgoneta i les estacions destí
        furgoneta.destins.append(self.estacio_desti)
        furgoneta.bicis_per_desti[self.estacio_desti] = bicis_a_enviar_desti1
        estacions.lista_estaciones[self.estacio_desti].num_bicicletas_no_usadas += bicis_a_enviar_desti1
        
        if self.estacio_desti2:
            furgoneta.destins.append(self.estacio_desti2)
            furgoneta.bicis_per_desti[self.estacio_desti2] = bicis_a_enviar_desti2
            estacions.lista_estaciones[self.estacio_desti2].num_bicicletas_no_usadas += bicis_a_enviar_desti2

            
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
    
    def executa(self):
        assert self.estacio_desti2 is not None
        self.estacio_desti, self.estacio_desti2 = self.estacio_desti2, self.estacio_desti
        