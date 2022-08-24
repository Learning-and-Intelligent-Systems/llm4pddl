(define (problem freecell3-4)
  (:domain freecell)
  (:objects
    club - object
    club0 - object
    cluba - object
    diamond - object
    diamond0 - object
    diamond2 - object
    diamonda - object
    heart - object
    heart0 - object
    heart2 - object
    heart3 - object
    hearta - object
    n0 - object
    n1 - object
    n2 - object
    n3 - object
    spade3 - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (successor n3 n2)
    (clear spade3)
    (on spade3 heart2)
    (on heart2 hearta)
    (bottomcol hearta)
    (clear cluba)
    (on cluba diamonda)
    (bottomcol diamonda)
    (clear heart3)
    (on heart3 diamond2)
    (colspace n0)
    (value cluba n1)
    (suit cluba club)
    (value heart3 n3)
    (suit heart3 heart)
    (value heart2 n2)
    (suit heart2 heart)
    (canstack heart2 spade3)
    (value diamonda n1)
    (suit diamonda diamond)
    (value hearta n1)
    (suit hearta heart)
    (home diamond0)
    (value diamond0 n0)
    (suit diamond0 diamond)
    (home club0)
    (value club0 n0)
    (suit club0 club)
    (home heart0)
    (value heart0 n0)
    (suit heart0 heart)
  )
  (:goal (and (home heart3)))
)
