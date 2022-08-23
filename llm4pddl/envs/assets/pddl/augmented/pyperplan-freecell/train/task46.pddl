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
    diamond2 - object
    diamond3 - object
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
    spade - object
    spade0 - object
    spade2 - object
    spade3 - object
    spadea - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (successor n3 n2)
    (clear spade3)
    (on spade3 heart2)
    (on heart2 hearta)
    (bottomcol hearta)
    (clear club2)
    (on club2 diamond3)
    (on diamond3 spadea)
    (bottomcol spadea)
    (clear spade2)
    (on spade2 club3)
    (clear cluba)
    (on cluba diamonda)
    (bottomcol diamonda)
    (clear heart3)
    (on heart3 diamond2)
    (bottomcol diamond2)
    (colspace n0)
    (value spade3 n3)
    (suit spade3 spade)
    (value spade2 n2)
    (suit spade2 spade)
    (value cluba n1)
    (suit cluba club)
    (value heart3 n3)
    (suit heart3 heart)
    (value heart2 n2)
    (suit heart2 heart)
    (value diamond3 n3)
    (suit diamond3 diamond)
    (value diamonda n1)
    (suit diamonda diamond)
    (value diamond2 n2)
    (suit diamond2 diamond)
    (value hearta n1)
    (suit hearta heart)
    (value spadea n1)
    (suit spadea spade)
    (home diamond0)
    (value diamond0 n0)
    (suit diamond0 diamond)
    (home club0)
    (value club0 n0)
    (suit club0 club)
    (home heart0)
    (value heart0 n0)
    (suit heart0 heart)
    (home spade0)
    (value spade0 n0)
    (suit spade0 spade)
  )
  (:goal (and (home diamond3) (home heart3)))
)
