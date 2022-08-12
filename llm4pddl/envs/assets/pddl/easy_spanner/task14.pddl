(define (problem task14) (:domain easy_spanner)
  (:objects
    bob - man
    gate - location
    location0 - location
    location1 - location
    location2 - location
    nut0 - nut
    nut1 - nut
    shed - location
    spanner0 - spanner
    spanner1 - spanner
    spanner2 - spanner
    spanner3 - spanner
  )
  (:init
    (at bob shed)
    (at nut0 gate)
    (at nut1 gate)
    (at spanner0 location1)
    (at spanner1 location0)
    (at spanner2 location1)
    (at spanner3 location2)
    (link location0 location1)
    (link location1 location2)
    (link location2 gate)
    (link shed location0)
    (loose nut0)
    (loose nut1)
    (useable spanner0)
    (useable spanner1)
    (useable spanner2)
    (useable spanner3)
  )
  (:goal (and (tightened nut0)
    (tightened nut1)))
)
