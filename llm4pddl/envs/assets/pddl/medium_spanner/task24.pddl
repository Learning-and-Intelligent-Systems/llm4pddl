(define (problem task24) (:domain medium_spanner)
  (:objects
    bob - man
    gate - location
    location0 - location
    location1 - location
    location2 - location
    location3 - location
    location4 - location
    nut0 - nut
    nut1 - nut
    nut2 - nut
    nut3 - nut
    nut4 - nut
    nut5 - nut
    nut6 - nut
    shed - location
    spanner0 - spanner
    spanner1 - spanner
    spanner10 - spanner
    spanner11 - spanner
    spanner2 - spanner
    spanner3 - spanner
    spanner4 - spanner
    spanner5 - spanner
    spanner6 - spanner
    spanner7 - spanner
    spanner8 - spanner
    spanner9 - spanner
  )
  (:init
    (at bob shed)
    (at nut0 gate)
    (at nut1 gate)
    (at nut2 gate)
    (at nut3 gate)
    (at nut4 gate)
    (at nut5 gate)
    (at nut6 gate)
    (at spanner0 location0)
    (at spanner10 location4)
    (at spanner11 location1)
    (at spanner1 location0)
    (at spanner2 location2)
    (at spanner3 location0)
    (at spanner4 location3)
    (at spanner5 location1)
    (at spanner6 location4)
    (at spanner7 location2)
    (at spanner8 location3)
    (at spanner9 location0)
    (link location0 location1)
    (link location1 location2)
    (link location2 location3)
    (link location3 location4)
    (link location4 gate)
    (link shed location0)
    (loose nut0)
    (loose nut1)
    (loose nut2)
    (loose nut3)
    (loose nut4)
    (loose nut5)
    (loose nut6)
    (useable spanner0)
    (useable spanner10)
    (useable spanner11)
    (useable spanner1)
    (useable spanner2)
    (useable spanner3)
    (useable spanner4)
    (useable spanner5)
    (useable spanner6)
    (useable spanner7)
    (useable spanner8)
    (useable spanner9)
  )
  (:goal (and (tightened nut0)
    (tightened nut1)
    (tightened nut2)
    (tightened nut3)
    (tightened nut4)
    (tightened nut5)
    (tightened nut6)))
)
