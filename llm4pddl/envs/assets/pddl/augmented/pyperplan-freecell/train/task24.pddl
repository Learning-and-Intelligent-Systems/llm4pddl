(define (problem freecell2-4)
  (:domain freecell)
  (:objects
    cluba - object
    diamond - object
    diamond0 - object
    diamonda - object
    heart - object
    heart0 - object
    heart2 - object
    hearta - object
    n0 - object
    n1 - object
    n2 - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (clear diamonda)
    (on diamonda hearta)
    (bottomcol hearta)
    (clear heart2)
    (on heart2 cluba)
    (colspace n0)
    (value diamonda n1)
    (suit diamonda diamond)
    (value heart2 n2)
    (suit heart2 heart)
    (value hearta n1)
    (suit hearta heart)
    (home diamond0)
    (value diamond0 n0)
    (suit diamond0 diamond)
    (home heart0)
    (value heart0 n0)
    (suit heart0 heart)
  )
  (:goal (and (home heart2)))
)