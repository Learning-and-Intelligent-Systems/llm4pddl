(define (problem freecell5-4)
  (:domain freecell)
  (:objects
    club - object
    club0 - object
    club2 - object
    club3 - object
    club4 - object
    cluba - object
    diamond - object
    diamond0 - object
    diamond2 - object
    diamond3 - object
    diamond5 - object
    diamonda - object
    heart - object
    heart0 - object
    heart2 - object
    heart4 - object
    hearta - object
    n0 - object
    n1 - object
    n2 - object
    n3 - object
    n4 - object
    n5 - object
    spade - object
    spade0 - object
    spade2 - object
    spade3 - object
    spade4 - object
    spade5 - object
    spadea - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (successor n3 n2)
    (successor n4 n3)
    (successor n5 n4)
    (cellspace n2)
    (clear club2)
    (on club2 diamond3)
    (on diamond3 hearta)
    (on hearta spadea)
    (bottomcol spadea)
    (clear heart4)
    (on heart4 spade5)
    (on spade5 diamonda)
    (on diamonda spade2)
    (bottomcol spade2)
    (clear club3)
    (on club3 club4)
    (on club4 heart2)
    (on heart2 cluba)
    (bottomcol cluba)
    (clear spade4)
    (on spade4 diamond2)
    (on diamond2 diamond5)
    (on diamond5 spade3)
    (bottomcol spade3)
    (colspace n0)
    (value club2 n2)
    (suit club2 club)
    (value club3 n3)
    (suit club3 club)
    (value spade4 n4)
    (suit spade4 spade)
    (canstack diamond3 spade4)
    (value spade5 n5)
    (suit spade5 spade)
    (value diamond2 n2)
    (suit diamond2 diamond)
    (value hearta n1)
    (suit hearta heart)
    (value diamonda n1)
    (suit diamonda diamond)
    (value heart2 n2)
    (suit heart2 heart)
    (value spadea n1)
    (suit spadea spade)
    (value spade2 n2)
    (suit spade2 spade)
    (value cluba n1)
    (suit cluba club)
    (value spade3 n3)
    (suit spade3 spade)
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
  (:goal (and (home spade5)))
)
