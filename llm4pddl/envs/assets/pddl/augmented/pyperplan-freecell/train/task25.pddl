(define (problem freecell2-4)
  (:domain freecell)
  (:objects
    club2 - object
    diamond - object
    diamond0 - object
    diamond2 - object
    diamonda - object
    heart - object
    heart0 - object
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
    (clear club2)
    (on club2 diamond2)
    (bottomcol diamond2)
    (colspace n0)
    (value diamonda n1)
    (suit diamonda diamond)
    (value hearta n1)
    (suit hearta heart)
    (value diamond2 n2)
    (suit diamond2 diamond)
    (home diamond0)
    (value diamond0 n0)
    (suit diamond0 diamond)
    (home heart0)
    (value heart0 n0)
    (suit heart0 heart)
  )
  (:goal (and (home diamond2)))
)
