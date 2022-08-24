(define (problem logistics-5-0)
  (:domain logistics)
  (:objects
    apt2 - airport
    cit2 - city
    obj23 - package
    pos2 - location
    tru2 - truck
  )
  (:init
    (at tru2 pos2)
    (at obj23 pos2)
    (in-city pos2 cit2)
    (in-city apt2 cit2)
  )
  (:goal (and (at obj23 apt2)))
)
