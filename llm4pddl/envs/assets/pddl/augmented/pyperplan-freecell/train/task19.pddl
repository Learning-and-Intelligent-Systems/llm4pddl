(define (problem freecell2-4)
  (:domain freecell)
  (:objects
    cluba - object
    diamonda - object
    heart - object
    heart0 - object
    heart2 - object
    hearta - object
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
    (clear diamonda)
    (on diamonda hearta)
    (bottomcol hearta)
    (clear heart2)
    (on heart2 cluba)
    (colspace n0)
    (value spadea n1)
    (suit spadea spade)
    (value heart2 n2)
    (suit heart2 heart)
    (value spade2 n2)
    (suit spade2 spade)
    (value hearta n1)
    (suit hearta heart)
    (home heart0)
    (value heart0 n0)
    (suit heart0 heart)
    (home spade0)
    (value spade0 n0)
    (suit spade0 spade)
  )
  (:goal (and (home heart2)))
)
