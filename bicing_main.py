import random

from aima.search import hill_climbing

from bicing_estacions import Estacio, Estacions
from bicing_furgonetes import Furgoneta, Furgonetes

from bicing_parametres import Parametres
from bicing_problem import BicingProblem
from bicing_estat import Estat


# Funcions de generació dels diferents estats inicials


#42
suma_h = 0
iter = 1
for i in range(iter):
    
    params = Parametres(25, 1250, random.randint(2,5000), 5, 30)
    estacions = Estacions(params.n_estacions, params.n_bicis, params.llavor)

    estat_inicial = genera_estat_inicial(params, estacions) #Necessari executar per crear l'estat inicial

    #print('Heurística estat inicial: ', estat_inicial.h())

    n = hill_climbing(BicingProblem(estat_inicial))

    #print RUTA de les furgonetes

    suma_h += n.h()
    #print ('\nHeurística estat inicial', n.h() ) # Valor de l’estat final


mitjana = suma_h / iter
print('Heurística mitjana: ', mitjana)