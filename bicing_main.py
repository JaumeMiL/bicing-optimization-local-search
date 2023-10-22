import random
import time

from aima.search import hill_climbing, simulated_annealing
from abia_bicing import Estaciones
from bicing_parametres import Parametres
from bicing_problem import *
from bicing_estat import genera_estat_inicial_1, genera_estat_inicial_0, genera_estat_inicial_2, Estat


params = Parametres(25, 1250, random.randint(2,5000), 5, 30)
estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)

estat_inicial = genera_estat_inicial_0(params, estacions)
h_inicial = estat_inicial.heuristica1()
n = hill_climbing(BicingProblem(estat_inicial))
#sa = simulated_annealing(BicingProblem(estat_inicial))
print(f"\nEstat 0: \n  Inicial: {h_inicial}€ Final: {n.heuristica1()} €")

estat_inicial = genera_estat_inicial_1(params, estacions)
h_inicial = estat_inicial.heuristica2()
#n = hill_climbing(BicingProblem(estat_inicial))
#sa = simulated_annealing(BicingProblem(estat_inicial))
print(f"\nEstat 1: \n  Inicial: {h_inicial}€")

estat_inicial = genera_estat_inicial_2(params, estacions)
h_inicial = estat_inicial.heuristica2()
#n = hill_climbing(BicingProblem(estat_inicial))
#sa = simulated_annealing(BicingProblem(estat_inicial))
print(f"\nEstat 2: \n  Inicial: {h_inicial}€")
