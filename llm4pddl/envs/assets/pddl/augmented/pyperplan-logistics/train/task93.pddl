(define (problem logistics-5-1)
  (:domain logistics)
  (:objects
    apt1 - airport
    cit1 - city
    obj12 - package
    pos1 - location
    tru1 - truck
  )
  (:init
    (at tru1 pos1)
    (at obj12 pos1)
    (in-city pos1 cit1)
    (in-city apt1 cit1)
  )
  (:goal (and (at obj12 apt1)))
)
