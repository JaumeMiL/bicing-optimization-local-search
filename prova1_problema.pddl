(define (problem problema_llibres1)
  (:domain llibres1)
  
  (:objects
    llibre1 - no_te_predecesor
    llibre2 - no_te_predecesor
    llibre3 - no_te_predecesor
    llibre4 - te_predecesor
    llibre5 - no_te_predecesor
    llibre6 - te_predecesor
  )

  (:init
    (not (llegit llibre1))
    (not (llegit llibre2))
    (not (llegit llibre3))
    (not (llegit llibre4))
    (not (llegit llibre5))
    (not (llegit llibre6))
    (predecesor llibre2 llibre6)
    (predecesor llibre3 llibre4)
    (llibre_desitjat llibre4)
    (llibre_desitjat llibre5)
    (llibre_desitjat llibre6)
  )

  (:goal (forall (?llibre - llibre)
             (or (not (llibre_desitjat ?llibre))
                 (llegit ?llibre))))
)
