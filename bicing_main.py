import random
import time
from aima.search import hill_climbing
from abia_bicing import Estaciones
from bicing_parametres import Parametres
from bicing_problem import BicingProblem
from bicing_estat import genera_estat_inicial_1, genera_estat_inicial_0, genera_estat_inicial_2, Estat, dist_estacions

"""""""""
params = Parametres(25, 1250, 42, 5, 30)
estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)

estat_inicial = genera_estat_inicial_0(params, estacions)
h_inicial = estat_inicial.heuristica1()
n = hill_climbing(BicingProblem(estat_inicial))
print(f"\nEstat 0: \n  Inicial: {h_inicial}€ Final: {n.heuristica1()} €")

estat_inicial = genera_estat_inicial_1(params, estacions)
h_inicial = estat_inicial.heuristica2()
n = hill_climbing(BicingProblem(estat_inicial))
print(f"\nEstat 1: \n  Inicial: {h_inicial}€")
for Furgonetes in estat_inicial.flota:
    print(Furgonetes)

estat_inicial = genera_estat_inicial_2(params, estacions)print(f"FURGONETES FINAL")
h_inicial = estat_inicial.heuristica2()
#n = hill_climbing(BicingProblem(estat_inicial))
print(f"\nEstat 2: \n  Inicial: {h_inicial}€")
for Furgonetes in estat_inicial.flota:
    print(Furgonetes)

    """

#EXPERIMENT 7
params = Parametres(25, 1250, 42, 5, 30)
estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)

time_start = time.time()
estat_inicial = genera_estat_inicial_1(params, estacions) #estat inicial bo = 2
h_inicial = estat_inicial.heuristica1()
n = hill_climbing(BicingProblem(estat_inicial))
h_final = n.heuristica1()
time_end = time.time()

total_time = time_end - time_start

recorregut_total = 0
for furgoneta in estat_inicial.flota:
    recorregut_furgo = dist_estacions(furgoneta.origen, furgoneta.primera_est)
    if furgoneta.segona_est is not None:
        recorregut_furgo += dist_estacions(furgoneta.primera_est, furgoneta.segona_est)
    recorregut_total += recorregut_furgo

print(f"\nEXPERIMENT 7: \nBenefici_inicial: {h_inicial}€ Benefici_final: {n.heuristica1()}€")
print(f"\nTemps: {total_time} ms")
print(f"\nRecorregut: {recorregut_total} m")
print(f"Nombre d'estats Generats: {Estat.Contador_Estats}")
print(f"FURGONETES INICI")
for Furgonetes in estat_inicial.flota:
    print(Furgonetes)
print(f"FURGONETES FINAL")
for Furgonetes in n.flota:
    print(Furgonetes)

#EXPERIMENT 4
