(define (problem freecell4-4)
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
    diamond4 - object
    diamonda - object
    heart - object
    heart0 - object
    heart2 - object
    heart3 - object
    heart4 - object
    hearta - object
    n0 - object
    n1 - object
    n2 - object
    n3 - object
    n4 - object
    spade - object
    spade0 - object
    spade2 - object
    spade3 - object
    spade4 - object
    spadea - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (successor n3 n2)
    (successor n4 n3)
    (clear club3)
    (on club3 spade3)
    (on spade3 heart2)
    (on heart2 spade4)
    (clear diamond2)
    (on diamond2 cluba)
    (on cluba heart4)
    (clear heart3)
    (on heart3 spadea)
    (on spadea hearta)
    (bottomcol hearta)
    (clear diamond4)
    (on diamond4 diamond3)
    (on diamond3 club2)
    (clear diamonda)
    (on diamonda spade2)
    (on spade2 club4)
    (colspace n0)
    (canstack club3 heart4)
    (value diamond2 n2)
    (suit diamond2 diamond)
    (canstack heart3 spade4)
    (value diamond4 n4)
    (suit diamond4 diamond)
    (value diamonda n1)
    (suit diamonda diamond)
    (value spade3 n3)
    (suit spade3 spade)
    (canstack spade3 diamond4)
    (value cluba n1)
    (suit cluba club)
    (value spadea n1)
    (suit spadea spade)
    (value diamond3 n3)
    (suit diamond3 diamond)
    (value spade2 n2)
    (suit spade2 spade)
    (value heart2 n2)
    (suit heart2 heart)
    (canstack heart2 spade3)
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
    (home spade0)
    (value spade0 n0)
    (suit spade0 spade)
  )
  (:goal (and (home diamond4)))
)
