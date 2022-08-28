(define (problem freecell6-4)
  (:domain freecell)
  (:objects
    club - object
    club0 - object
    club2 - object
    club3 - object
    club4 - object
    club5 - object
    club6 - object
    cluba - object
    diamond - object
    diamond0 - object
    diamond2 - object
    diamond3 - object
    diamond4 - object
    diamond5 - object
    diamond6 - object
    diamonda - object
    heart - object
    heart0 - object
    heart2 - object
    heart3 - object
    heart4 - object
    heart5 - object
    heart6 - object
    hearta - object
    n0 - object
    n1 - object
    n2 - object
    n3 - object
    n4 - object
    n5 - object
    n6 - object
    spade - object
    spade0 - object
    spade2 - object
    spade3 - object
    spade4 - object
    spade5 - object
    spade6 - object
    spadea - object
  )
  (:init
    (successor n1 n0)
    (successor n2 n1)
    (successor n3 n2)
    (successor n4 n3)
    (successor n5 n4)
    (successor n6 n5)
    (cellspace n3)
    (clear heart6)
    (on heart6 heart2)
    (on heart2 hearta)
    (on hearta club4)
    (on club4 diamonda)
    (bottomcol diamonda)
    (clear diamond3)
    (on diamond3 diamond5)
    (on diamond5 club6)
    (on club6 diamond6)
    (on diamond6 heart3)
    (bottomcol heart3)
    (clear spadea)
    (on spadea heart4)
    (on heart4 spade4)
    (on spade4 cluba)
    (on cluba diamond4)
    (bottomcol diamond4)
    (clear spade3)
    (on spade3 spade6)
    (on spade6 heart5)
    (on heart5 club3)
    (on club3 diamond2)
    (bottomcol diamond2)
    (clear spade5)
    (on spade5 club2)
    (on club2 spade2)
    (on spade2 club5)
    (bottomcol club5)
    (colspace n0)
    (value heart6 n6)
    (suit heart6 heart)
    (value diamond3 n3)
    (suit diamond3 diamond)
    (value spadea n1)
    (suit spadea spade)
    (value spade3 n3)
    (suit spade3 spade)
    (value spade5 n5)
    (suit spade5 spade)
    (value heart2 n2)
    (suit heart2 heart)
    (value diamond5 n5)
    (suit diamond5 diamond)
    (value heart4 n4)
    (suit heart4 heart)
    (value spade6 n6)
    (suit spade6 spade)
    (value club2 n2)
    (suit club2 club)
    (value hearta n1)
    (suit hearta heart)
    (value club6 n6)
    (suit club6 club)
    (value spade4 n4)
    (suit spade4 spade)
    (value heart5 n5)
    (suit heart5 heart)
    (value spade2 n2)
    (suit spade2 spade)
    (value club4 n4)
    (suit club4 club)
    (value diamond6 n6)
    (suit diamond6 diamond)
    (value cluba n1)
    (suit cluba club)
    (value club3 n3)
    (suit club3 club)
    (value club5 n5)
    (suit club5 club)
    (value diamonda n1)
    (suit diamonda diamond)
    (value heart3 n3)
    (suit heart3 heart)
    (value diamond4 n4)
    (suit diamond4 diamond)
    (value diamond2 n2)
    (suit diamond2 diamond)
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
  (:goal (and (home diamond6) (home club6) (home heart6) (home spade6)))
)
