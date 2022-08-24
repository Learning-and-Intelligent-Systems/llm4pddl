(define (problem logistics-4-0)
  (:domain logistics)
  (:objects
    apt1 - airport
    cit1 - city
    obj11 - package
    pos1 - location
    tru1 - truck
  )
  (:init
    (at tru1 pos1)
    (at obj11 pos1)
    (in-city pos1 cit1)
    (in-city apt1 cit1)
  )
  (:goal (and (at obj11 apt1)))
)
