import random
import time
from aima.search import hill_climbing, simulated_annealing
from abia_bicing import Estaciones
from bicing_parametres import Parametres
from bicing_problem import BicingProblem1, BicingProblem2
from bicing_estat import genera_estat_inicial_1, genera_estat_inicial_0, genera_estat_inicial_2, Estat, dist_estacions

print("Escull quin experiment vols fer introduïnt el número corresponent a la llista que tens a baix")
print(" 1: Experiment 1 \n 2: Experiment 2 \n 3: Experiment 3 \n 4: Experiment 4 \n 5: Experiment 5 \n 6: Experiment 6 \n 7: Experiment Especial")
valor = int(input())


if valor == 1:
    #Experiment 1
    print(f"\nEXPERIMENT 1: \n")
    params = Parametres(25, 1250, random.randint(1, 25000), 5, 30)
    estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
    time_start = time.time()
    estat_inicial = genera_estat_inicial_0(params, estacions)
    h_inicial = estat_inicial.heuristica1()
    print(f"Furgonetes que tenim inicialment:")
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

    print(f"\nEXPERIMENT 1: \nBenefici_inicial: {h_inicial}€ Benefici_final: {h_final}€")
    print(f"\nTemps total del problema: {total_time} ms")
    print(f"\nRecorregut total de les furgonetes: {recorregut_total} m")
    print(f"Nombre d'estats generats: {Estat.Contador_Estats}")
    print(f"Furgonetes que tenim al final:")
    for Furgonetes in n.flota:
        print(Furgonetes)
#Experiment 2
elif valor == 2:
    print(f"\nEXPERIMENT 2: \n")
    print(f"\nESTAT INICIAL 0: \n")
    #Estat inicial 0
    params = Parametres(25, 1250, random.randint(1, 25000), 5, 30)
    estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
    time_start = time.time()
    estat_inicial = genera_estat_inicial_0(params, estacions)
    h_inicial = estat_inicial.heuristica1()
    print(f"Furgonetes que tenim inicialment a l'estat inicial 0:")
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

    print(f"\nEXPERIMENT 2 ESTAT INICIAL 0: \nBenefici_inicial: {h_inicial}€ Benefici_final: {h_final}€")
    print(f"\nTemps total del problema: {total_time} ms")
    print(f"\nRecorregut total de les furgonetes: {recorregut_total} m")
    print(f"Nombre d'estats generats: {Estat.Contador_Estats}")
    print(f"Furgonetes que tenim al final:")
    for Furgonetes in n.flota:
        print(Furgonetes)

    
    print(f"\nESTAT INICIAL 1: \n")
    #Estat inicial 1
    params = Parametres(25, 1250, random.randint(1, 25000), 5, 30)
    estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
    time_start = time.time()
    estat_inicial = genera_estat_inicial_1(params, estacions)
    h_inicial = estat_inicial.heuristica1()
    print(f"Furgonetes que tenim inicialment a l'estat inicial 1:")
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

    print(f"\nEXPERIMENT 2 ESTAT INICIAL 1: \nBenefici_inicial: {h_inicial}€ Benefici_final: {h_final}€")
    print(f"\nTemps total del problema: {total_time} ms")
    print(f"\nRecorregut total de les furgonetes: {recorregut_total} m")
    print(f"Nombre d'estats generats: {Estat.Contador_Estats}")
    print(f"Furgonetes que tenim al final:")
    for Furgonetes in n.flota:
        print(Furgonetes)
    
    print(f"\nESTAT INICIAL 2: \n")    
    #Estat inicial 2
    params = Parametres(25, 1250, random.randint(1, 25000), 5, 30)
    estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
    time_start = time.time()
    estat_inicial = genera_estat_inicial_2(params, estacions)
    h_inicial = estat_inicial.heuristica1()
    print(f"Furgonetes que tenim inicialment a l'estat inicial 2:")
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

    print(f"\nEXPERIMENT 2 ESTAT INICIAL 2: \nBenefici_inicial: {h_inicial}€ Benefici_final: {h_final}€")
    print(f"\nTemps total del problema: {total_time} ms")
    print(f"\nRecorregut total de les furgonetes: {recorregut_total} m")
    print(f"Nombre d'estats generats: {Estat.Contador_Estats}")
    print(f"Furgonetes que tenim al final:")
    for Furgonetes in n.flota:
        print(Furgonetes)


elif valor == 3 or valor == 5:
    print(f"Malauradament al dedicar tant de temps a intentar trobar l'error del nostre Hill Climbing, no hem implementar correctament el Simmulated Annealing cosa que no ens ha permès fer els experiments relacionats amb aquesta tècnica.")

elif valor == 4:
    print(f"\nEXPERIMENT 4: Evolució del temps d'execució en funció del nombre d'estacions, furgonetes i bicicletes\n")

    max_estacions = 200  
    increment_estacions = 25

    for estacions_actuals in range(25, max_estacions + 1, increment_estacions):
        bicis_actuals = estacions_actuals * 50
        furgonetes_actuals = estacions_actuals // 5
        
        print(f"\nAmb {estacions_actuals} estacions, {furgonetes_actuals} furgonetes i {bicis_actuals} bicicletes:\n")
        
        params = Parametres(estacions_actuals, bicis_actuals, random.randint(1, 25000), furgonetes_actuals, 30)
        estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
        
        time_start = time.time()
        estat_inicial = genera_estat_inicial_0(params, estacions) 
        
        n = hill_climbing(BicingProblem1(estat_inicial))
        time_end = time.time()
        
        total_time = time_end - time_start
        print(f"Temps d'execució amb {estacions_actuals} estacions: {total_time} ms\n")


elif valor == 6:
    print(f"\nEXPERIMENT 6 \n")

elif valor == 7:
    print(f"\nEXPERIMENT ESPECIAL: \n")
    params = Parametres(25, 1250, 42, 5, 30)
    estacions = Estaciones(params.n_estacions, params.n_bicis, params.llavor)
    time_start = time.time()
    estat_inicial = genera_estat_inicial_0(params, estacions)
    h_inicial = estat_inicial.heuristica1()
    print(f"Furgonetes que tenim inicialment:")
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

    print(f"\nBenefici_inicial: {h_inicial}€ Benefici_final: {h_final}€")
    print(f"\nTemps total del problema: {total_time} ms")
    print(f"\nRecorregut total de les furgonetes: {recorregut_total} m")
    print(f"Nombre d'estats generats: {Estat.Contador_Estats}")
    print(f"Furgonetes que tenim al final:")
    for Furgonetes in n.flota:
        print(Furgonetes)
