(define (problem task3) (:domain easy_spanner)
  (:objects
    bob - man
    gate - location
    location0 - location
    nut0 - nut
    shed - location
    spanner0 - spanner
  )
  (:init
    (at bob shed)
    (at nut0 gate)
    (at spanner0 location0)
    (link location0 gate)
    (link shed location0)
    (loose nut0)
    (useable spanner0)
  )
  (:goal (and (tightened nut0)))
)
