
from bicing_furgonetes import Furgonetes
from abia_bicing import Estacion

class Operadors:
    pass



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

    
class Afegir_Furgoneta(Operadors):
    def __init__(self):
        pass
    def __repr__(self):
        return f"Ageigeix una nova furgoneta"


class Esborrar_Furgoneta(Operadors):
    def __init__(self, estacio_origen: Estacion):
        self.estacio_origen = estacio_origen

    def __repr__(self) -> str:
        return f"Suprimeix la furgoneta amb estació d'origen {self.estacio_origen}"

#NOUS OPERADORS CREATS DIA 22/10

#Aquest operador en cas de ser possible carrega dues bicicletes més que descarregarà a l'estació 1 i a l'estació 2
class Carregar_Dues_Bicicletes_Més(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str: 
        if self.estacio_desti2:
            return f"Carrega dues bicicletes més a la furgoneta l'estació i descarrega una més a l'estació {self.estacio_desti} i {self.estacio_desti2}"
        else:
            return f"Carrega una bicicleta més a la furgoneta i descarrega-la a l'estació {self.estacio_desti}"


#Aquest operador en cas de ser possible treu dues bicicletes que anaven cada una a una estació diferent (a l'estació 1 i a l'estació 2)
class Carregar_Dues_Bicicletes_Menys(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str: 
        if self.estacio_desti2:
            return f"Carrega dues bicicletes menys a la furgoneta i descarrega una menys a l'estació {self.estacio_desti} i {self.estacio_desti2}"
        else:
            return f"Carrega una bicicleta menys a la furgoneta i descarrega'n una menys a l'estació {self.estacio_desti}"
        
#Aquest operador passa una bici que s'havia de descarregar a l'estació 1 a l'estació 2
class Bici_Estacio1_A_Estacio2(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str: 
        if self.estacio_desti2:
            return f"Una bicicleta que anava a l'estació {self.estacio_desti} ara anirà a l'estació {self.estacio_desti2}"
    
#Aquest operador passa una bici que s'havia de descarregar a l'estació 2 a l'estació 1
class Bici_Estacio2_A_Estacio1(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int = None):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        
    def __repr__(self) -> str: 
        if self.estacio_desti2:
            return f"Una bicicleta que anava a l'estació {self.estacio_desti2} ara anirà a l'estació {self.estacio_desti}"

class CanviaEst1(Operadors):
    
    def __init__(self, estacio_origen, estacio_desti, estacio_desti2, estacio_nova, lista_estaciones):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
        self.estacio_nova = estacio_nova
        self.lista_estaciones = lista_estaciones
    
    def __repr__(self) -> str: 
        return f"Canvia la primera estació de la furgoneta {self.estacio_desti}"
    
class CanviaEst2(Operadors):
    def __init__(self, estacio_origen: int, estacio_desti: int, estacio_desti2: int):
        self.estacio_origen = estacio_origen
        self.estacio_desti = estacio_desti
        self.estacio_desti2 = estacio_desti2
    
    def __repr__(self) -> str: 
        if self.estacio_desti2:
            return f"Canvia la segona estació de la furgoneta {self.estacio_desti2}"