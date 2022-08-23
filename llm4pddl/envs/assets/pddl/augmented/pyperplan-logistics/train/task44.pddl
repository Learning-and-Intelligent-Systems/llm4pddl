(define (problem logistics-4-0)
  (:domain logistics)
  (:objects
    apt1 - airport
    cit1 - city
    obj13 - package
    pos1 - location
    tru1 - truck
  )
  (:init
    (at tru1 pos1)
    (at obj13 pos1)
    (in-city pos1 cit1)
    (in-city apt1 cit1)
  )
  (:goal (and (at obj13 apt1)))
)
