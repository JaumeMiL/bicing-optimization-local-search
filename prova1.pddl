
(define (domain llibres1)
(:requirements :strips :fluents :adl)

(:types  te_predecesor no_te_predecesor - llibre ) 

(:predicates
(llegit ?x - llibre)
(llibre_desitjat ?x - llibre)
(predecesor ?x - no_te_predecesor ?y - te_predecesor) ;x es predecesor de y, x  no té predecesor ja que un llibre sol pot tenir un predecesor, per tant, si es predecesor d'un llibre no en pot tenir
)

(:action llegir_llibre_desitjat_sense_predecesor ;llegeix un llibre desitjat que no té predecesor
:parameters (?x - no_te_predecesor)
:precondition (and (llibre_desitjat ?x) (not (llegit ?x)))
:effect (llegit ?x)
)

(:action llegir_llibre_desitjat_amb_predecesor ;llegeix un llibre desitjat que té predecesor
:parameters (?l1 - te_predecesor ?l2 - no_te_predecesor)
:precondition (and (llibre_desitjat ?l1) (not (llegit ?l1)) (llegit ?l2) (predecesor ?l2 ?l1))
:effect (llegit ?l1)
)

(:action llegir_llibre_predecesor_no_desitjat ;llegeix un llibre predecessor no desitjat quan es necessari per llegir-ne un de desitjat
:parameters (?l1 - no_te_predecesor ?l2 - te_predecesor)
:precondition (and (llibre_desitjat ?l2) (not (llibre_desitjat ?l1)) (not (llegit ?l1)) (not(llegit ?l2)) (predecesor ?l1 ?l2))
:effect (llegit ?l1)
)

)