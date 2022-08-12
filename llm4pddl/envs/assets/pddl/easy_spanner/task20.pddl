(define (problem task20) (:domain easy_spanner)
  (:objects
    bob - man
    gate - location
    location0 - location
    location1 - location
    nut0 - nut
    nut1 - nut
    nut2 - nut
    nut3 - nut
    shed - location
    spanner0 - spanner
    spanner1 - spanner
    spanner2 - spanner
    spanner3 - spanner
    spanner4 - spanner
    spanner5 - spanner
  )
  (:init
    (at bob shed)
    (at nut0 gate)
    (at nut1 gate)
    (at nut2 gate)
    (at nut3 gate)
    (at spanner0 location1)
    (at spanner1 location0)
    (at spanner2 location0)
    (at spanner3 location0)
    (at spanner4 location1)
    (at spanner5 location0)
    (link location0 location1)
    (link location1 gate)
    (link shed location0)
    (loose nut0)
    (loose nut1)
    (loose nut2)
    (loose nut3)
    (useable spanner0)
    (useable spanner1)
    (useable spanner2)
    (useable spanner3)
    (useable spanner4)
    (useable spanner5)
  )
  (:goal (and (tightened nut0)
    (tightened nut1)
    (tightened nut2)
    (tightened nut3)))
)
