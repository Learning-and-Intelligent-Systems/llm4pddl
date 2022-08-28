(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    infrared0 - object
    instrument1 - object
    instrument2 - object
    phenomenon8 - object
    phenomenon9 - object
    planet5 - object
    satellite1 - object
    star0 - object
    star2 - object
    thermograph2 - object
  )
  (:init
    (satellite satellite1)
    (instrument instrument1)
    (supports instrument1 infrared0)
    (calibration_target instrument1 star2)
    (instrument instrument2)
    (supports instrument2 thermograph2)
    (calibration_target instrument2 star2)
    (on_board instrument1 satellite1)
    (on_board instrument2 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star0)
    (mode infrared0)
    (mode thermograph2)
    (direction star0)
    (direction star2)
    (direction planet5)
    (direction phenomenon8)
    (direction phenomenon9)
  )
  (:goal (and (pointing satellite1 planet5) (have_image planet5 thermograph2) (have_image phenomenon8 thermograph2) (have_image phenomenon9 infrared0)))
)
