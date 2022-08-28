(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    instrument2 - object
    planet5 - object
    satellite1 - object
    star0 - object
    star2 - object
    thermograph2 - object
  )
  (:init
    (satellite satellite1)
    (instrument instrument2)
    (supports instrument2 thermograph2)
    (calibration_target instrument2 star2)
    (on_board instrument2 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star0)
    (mode thermograph2)
    (direction star0)
    (direction star2)
    (direction planet5)
  )
  (:goal (and (have_image planet5 thermograph2)))
)
