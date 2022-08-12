(define (problem task28) (:domain easy_spanner)
  (:objects
    bob - man
    gate - location
    location0 - location
    location1 - location
    nut0 - nut
    nut1 - nut
    shed - location
    spanner0 - spanner
    spanner1 - spanner
  )
  (:init
    (at bob shed)
    (at nut0 gate)
    (at nut1 gate)
    (at spanner0 location0)
    (at spanner1 location0)
    (link location0 location1)
    (link location1 gate)
    (link shed location0)
    (loose nut0)
    (loose nut1)
    (useable spanner0)
    (useable spanner1)
  )
  (:goal (and (tightened nut0)
    (tightened nut1)))
)
