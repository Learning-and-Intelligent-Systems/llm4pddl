(define (problem task11) (:domain medium_spanner)
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
    spanner2 - spanner
    spanner3 - spanner
    spanner4 - spanner
    spanner5 - spanner
    spanner6 - spanner
    spanner7 - spanner
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
    (at spanner0 location4)
    (at spanner1 location2)
    (at spanner2 location4)
    (at spanner3 location0)
    (at spanner4 location3)
    (at spanner5 location2)
    (at spanner6 location3)
    (at spanner7 location0)
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
    (useable spanner1)
    (useable spanner2)
    (useable spanner3)
    (useable spanner4)
    (useable spanner5)
    (useable spanner6)
    (useable spanner7)
  )
  (:goal (and (tightened nut0)
    (tightened nut1)
    (tightened nut2)
    (tightened nut3)
    (tightened nut4)
    (tightened nut5)
    (tightened nut6)))
)
