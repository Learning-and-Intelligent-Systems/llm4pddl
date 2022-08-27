(define (problem freecell2-4)
  (:domain freecell)
  (:objects
    club - object
    club0 - object
    club2 - object
    cluba - object
    diamond2 - object
    heart2 - object
    n0 - object
    n1 - object
    n2 - object
    spade - object
    spade0 - object
    spade2 - object
    spadea - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (clear spadea)
    (on spadea spade2)
    (bottomcol spade2)
    (clear club2)
    (on club2 diamond2)
    (clear heart2)
    (on heart2 cluba)
    (bottomcol cluba)
    (colspace n0)
    (value spadea n1)
    (suit spadea spade)
    (value club2 n2)
    (suit club2 club)
    (value spade2 n2)
    (suit spade2 spade)
    (value cluba n1)
    (suit cluba club)
    (home club0)
    (value club0 n0)
    (suit club0 club)
    (home spade0)
    (value spade0 n0)
    (suit spade0 spade)
  )
  (:goal (and (home club2)))
)
