(define (problem logistics-5-0)
  (:domain logistics)
  (:objects
    apn1 - airplane
    apt1 - airport
    apt2 - airport
    cit2 - city
    obj22 - package
    pos2 - location
    tru2 - truck
  )
  (:init
    (at apn1 apt1)
    (at tru2 pos2)
    (at obj22 pos2)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
  )
  (:goal (and (at obj22 apt1)))
)
