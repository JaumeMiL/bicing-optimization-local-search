
(define (domain llibres_ext1)
    (:requirements :strips :fluents :adl)

    (:types  te_predecesor no_te_predecesor - llibre
            mes - mes
    )


    (:predicates
        (llegit ?x - llibre)
        (llibre_desitjat ?x - llibre)
        (predecesor ?x - llibre ?y - llibre)
        (mes_actual ?x - mes)
        (mes_seguent ?x - mes ?y - mes) ;y es següent de x
        (llegit_en_mes ?x - llibre ?y - mes)
    )

    (:action llegir_llibre_desitjat_sense_predecesor
        :parameters (?x - no_te_predecesor ?m - mes)
        :precondition (and (llibre_desitjat ?x) (not (llegit ?x)) (mes_actual ?x))
        :effect (and (llegit ?x) (llegit_en_mes ?x ?m))
    )

    (:action llegir_llibre_desitjat_amb_predecesor
        :parameters (?l1 - llibre ?l2 - llibre ?m1 - mes ?m2 - mes)
        :precondition (and (llibre_desitjat ?l1) (not (llegit ?l1)) (llegit ?l2) (predecesor ?l2 ?l1) (llegit_en_mes ?l2 ?m2) (mes_actual ?m1)  (mes_seguent ?m2 ?m1))
        :effect (and((llegit ?l1) (llegit_en_mes ?l1 ?m1)))
    )

    (:action llegir_llibre_predecesor_no_desitjat
        :parameters (?l1 - llibre ?l2 - llibre ?m - mes)
        :precondition (and (llibre_desitjat ?l2) (not (llibre_desitjat ?l1)) (not (llegit ?l1)) (not (llegit ?l2)) (predecesor ?l1 ?l2) (mes_actual ?m))
        :effect (and (llegit ?l1) (llegit_en_mes ?l1 ?m))
    )
    (:action avançar_mes
        :parameters (?m1 - mes ?m2 - mes)
        :precondition (and (mes_actual ?m1) (mes_seguent ?m1 ?m2))
        :effect (and (not (mes_actual ?m1)) (mes_actual ?m2)) 
    )
   


)