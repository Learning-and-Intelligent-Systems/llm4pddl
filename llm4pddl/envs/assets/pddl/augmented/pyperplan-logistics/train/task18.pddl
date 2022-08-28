(define (problem logistics-4-1)
  (:domain logistics)
  (:objects
    apt2 - airport
    cit2 - city
    obj21 - package
    pos2 - location
    tru2 - truck
  )
  (:init
    (at tru2 pos2)
    (at obj21 pos2)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
  )
  (:goal (and (at obj21 apt2)))
)
