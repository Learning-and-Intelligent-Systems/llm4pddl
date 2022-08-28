(define (problem logistics-4-2)
  (:domain logistics)
  (:objects
    apn1 - airplane
    apt1 - airport
    apt2 - airport
    cit2 - city
    obj12 - package
    obj21 - package
    obj23 - package
    pos1 - location
    pos2 - location
    tru2 - truck
  )
  (:init
    (at apn1 apt1)
    (at obj12 pos1)
    (at tru2 pos2)
    (at obj21 pos2)
    (at obj23 pos2)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
  )
  (:goal (and (at obj21 apt1) (at obj23 pos2) (at obj12 pos1)))
)
