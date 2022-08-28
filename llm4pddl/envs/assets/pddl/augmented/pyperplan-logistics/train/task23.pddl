(define (problem logistics-4-1)
  (:domain logistics)
  (:objects
    apn1 - airplane
    apt1 - airport
    apt2 - airport
    cit1 - city
    obj12 - package
    pos1 - location
    tru1 - truck
  )
  (:init
    (at apn1 apt2)
    (at tru1 pos1)
    (at obj12 pos1)
    (in-city pos1 cit1)
    (in-city apt1 cit1)
  )
  (:goal (and (at obj12 apt2)))
)
