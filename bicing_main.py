import random
import time
from aima.search import hill_climbing, simulated_annealing
from abia_bicing import Estaciones
from bicing_parametres import Parametres
from bicing_problem import BicingProblem1, BicingProblem2
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
print("Escull quin experiment vols fer introduïnt el número corresponent a la llista que tens a baix")
print("1: Experiment 1, 2: Experiment 2, 3: Experiment 3, 4: Experiment 4, 5: Experiment 5, 6: Experiment 6, 7: Experiment Especial")
valor = int(input())

"""1. Determinar qué conjunto de operadores da mejores resultados para una función heurística
 que optimice el primer criterio (el transporte es gratis) con un escenario en el que el número
 de estaciones es 25, el número total de bicicletas es 1250 y el número de furgonetas es 5. 
 Deberéis usar el algoritmo de Hill Climbing. Escoged una de las estrategias de inicialización 
 de entre las que proponéis. A partir de estos resultados deberéis fijar los operadores para el 
 resto de experimentos."""
if valor == 1:
    #Experiment 1

    params = Parametres(25, 1250, random.randint(1, 25000), 5, 30)
    estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
    time_start = time.time()
    estat_inicial = genera_estat_inicial_0(params, estacions)
    h_inicial = estat_inicial.heuristica1()
    print(f"FURGONETES INICIALS")
    for Furgonetes_ini in estat_inicial.flota:
        print(Furgonetes_ini)

    n = hill_climbing(BicingProblem1(estat_inicial))
    h_final = n.heuristica1()
    time_end = time.time()

    total_time = time_end - time_start

    recorregut_total = 0
    for furgoneta in estat_inicial.flota:
        recorregut_furgo = dist_estacions(furgoneta.origen, furgoneta.primera_est)
        if furgoneta.segona_est is not None:
            recorregut_furgo += dist_estacions(furgoneta.primera_est, furgoneta.segona_est)
        recorregut_total += recorregut_furgo

    print(f"\nEXPERIMENT 7: \nBenefici_inicial: {h_inicial}€ Benefici_final: {h_final}€")
    print(f"\nTemps: {total_time} ms")
    print(f"\nRecorregut: {recorregut_total} m")
    print(f"Nombre d'estats Generats: {Estat.Contador_Estats}")
    print(f"FURGONETES FINALS")
    for Furgonetes in n.flota:
        print(Furgonetes)
elif valor == 2:
    pass
elif valor == 3:
    pass
elif valor == 4:
    pass
elif valor == 5:
    pass
elif valor == 6:
    pass
elif valor == 7:
    #EXPERIMENT 7
    params = Parametres(25, 1250, 42, 5, 30)
    estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
    time_start = time.time()
    estat_inicial = genera_estat_inicial_1(params, estacions)
    h_inicial = estat_inicial.heuristica2()
    print(f"FURGONETES INICIALS")
    for Furgonetes_ini in estat_inicial.flota:
        print(Furgonetes_ini)

    n = hill_climbing(BicingProblem2(estat_inicial))
    h_final = n.heuristica2()
    time_end = time.time()

    total_time = time_end - time_start

    recorregut_total = 0
    for furgoneta in estat_inicial.flota:
        recorregut_furgo = dist_estacions(furgoneta.origen, furgoneta.primera_est)
        if furgoneta.segona_est is not None:
            recorregut_furgo += dist_estacions(furgoneta.primera_est, furgoneta.segona_est)
        recorregut_total += recorregut_furgo

    print(f"\nEXPERIMENT 7: \nBenefici_inicial: {h_inicial}€ Benefici_final: {h_final}€")
    print(f"\nTemps: {total_time} ms")
    print(f"\nRecorregut: {recorregut_total} m")
    print(f"Nombre d'estats Generats: {Estat.Contador_Estats}")
    print(f"FURGONETES FINALS")
    for Furgonetes in n.flota:
        print(Furgonetes)
