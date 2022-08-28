(define (problem freecell3-4)
  (:domain freecell)
  (:objects
    club - object
    club0 - object
    club2 - object
    cluba - object
    diamond - object
    diamond0 - object
    diamond2 - object
    diamond3 - object
    diamonda - object
    heart3 - object
    n0 - object
    n1 - object
    n2 - object
    n3 - object
    spadea - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (successor n3 n2)
    (clear club2)
    (on club2 diamond3)
    (on diamond3 spadea)
    (clear cluba)
    (on cluba diamonda)
    (bottomcol diamonda)
    (clear heart3)
    (on heart3 diamond2)
    (bottomcol diamond2)
    (colspace n0)
    (value cluba n1)
    (suit cluba club)
    (value diamond3 n3)
    (suit diamond3 diamond)
    (value diamonda n1)
    (suit diamonda diamond)
    (value diamond2 n2)
    (suit diamond2 diamond)
    (home diamond0)
    (value diamond0 n0)
    (suit diamond0 diamond)
    (home club0)
    (value club0 n0)
    (suit club0 club)
  )
  (:goal (and (home diamond3)))
)
