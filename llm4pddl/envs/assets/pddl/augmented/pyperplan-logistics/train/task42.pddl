(define (problem logistics-4-0)
  (:domain logistics)
  (:objects
    apn1 - airplane
    apt1 - airport
    apt2 - airport
    cit1 - city
    cit2 - city
    obj13 - package
    obj23 - package
    pos1 - location
    pos2 - location
    tru1 - truck
    tru2 - truck
  )
  (:init
    (at apn1 apt2)
    (at tru1 pos1)
    (at obj13 pos1)
    (at tru2 pos2)
    (at obj23 pos2)
    (in-city pos1 cit1)
    (in-city apt1 cit1)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
  )
  (:goal (and (at obj23 pos1) (at obj13 apt1)))
)
