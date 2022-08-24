(define (problem logistics-5-1)
  (:domain logistics)
  (:objects
    apt2 - airport
    cit2 - city
    obj21 - package
    obj22 - package
    pos2 - location
    tru2 - truck
  )
  (:init
    (at tru2 pos2)
    (at obj21 pos2)
    (at obj22 pos2)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
  )
  (:goal (and (at obj22 apt2) (at obj21 apt2)))
)
