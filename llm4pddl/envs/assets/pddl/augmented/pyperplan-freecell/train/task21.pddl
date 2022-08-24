(define (problem freecell2-4)
  (:domain freecell)
  (:objects
    club2 - object
    diamond - object
    diamond0 - object
    diamond2 - object
    diamonda - object
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
    (clear club2)
    (on club2 diamond2)
    (bottomcol diamond2)
    (colspace n0)
    (value spadea n1)
    (suit spadea spade)
    (value diamonda n1)
    (suit diamonda diamond)
    (value spade2 n2)
    (suit spade2 spade)
    (value diamond2 n2)
    (suit diamond2 diamond)
    (home diamond0)
    (value diamond0 n0)
    (suit diamond0 diamond)
    (home spade0)
    (value spade0 n0)
    (suit spade0 spade)
  )
  (:goal (and (home diamond2) (home spade2)))
)
