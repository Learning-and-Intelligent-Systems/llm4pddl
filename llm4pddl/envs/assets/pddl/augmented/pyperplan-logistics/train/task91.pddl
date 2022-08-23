(define (problem logistics-5-1)
  (:domain logistics)
  (:objects
    apt2 - airport
    cit2 - city
    obj11 - package
    obj22 - package
    pos1 - location
    pos2 - location
    tru2 - truck
  )
  (:init
    (at obj11 pos1)
    (at tru2 pos2)
    (at obj22 pos2)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
  )
  (:goal (and (at obj11 pos1) (at obj22 apt2)))
)
