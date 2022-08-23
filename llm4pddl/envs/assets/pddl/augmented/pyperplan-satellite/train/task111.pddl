(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    planet5 - object
    satellite1 - object
    star0 - object
  )
  (:init
    (satellite satellite1)
    (pointing satellite1 star0)
    (direction star0)
    (direction planet5)
  )
  (:goal (and (pointing satellite1 planet5)))
)
