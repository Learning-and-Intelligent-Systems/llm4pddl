(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    phenomenon5 - object
    satellite0 - object
    star4 - object
  )
  (:init
    (satellite satellite0)
    (pointing satellite0 star4)
    (direction star4)
    (direction phenomenon5)
  )
  (:goal (and (pointing satellite0 phenomenon5)))
)
