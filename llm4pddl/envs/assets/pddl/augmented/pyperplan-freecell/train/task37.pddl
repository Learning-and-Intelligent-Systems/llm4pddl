(define (problem freecell3-4)
  (:domain freecell)
  (:objects
    club - object
    club0 - object
    club2 - object
    club3 - object
    cluba - object
    diamond - object
    diamond0 - object
    diamond3 - object
    diamonda - object
    n0 - object
    n1 - object
    n2 - object
    n3 - object
    spade2 - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (successor n3 n2)
    (clear club2)
    (on club2 diamond3)
    (clear spade2)
    (on spade2 club3)
    (bottomcol club3)
    (clear cluba)
    (on cluba diamonda)
    (bottomcol diamonda)
    (colspace n0)
    (value club2 n2)
    (suit club2 club)
    (value cluba n1)
    (suit cluba club)
    (value club3 n3)
    (suit club3 club)
    (value diamonda n1)
    (suit diamonda diamond)
    (home diamond0)
    (value diamond0 n0)
    (suit diamond0 diamond)
    (home club0)
    (value club0 n0)
    (suit club0 club)
  )
  (:goal (and (home club3)))
)
