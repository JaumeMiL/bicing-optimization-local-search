
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
