(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    infrared0 - object
    instrument1 - object
    phenomenon9 - object
    planet5 - object
    satellite1 - object
    star0 - object
    star2 - object
  )
  (:init
    (satellite satellite1)
    (instrument instrument1)
    (supports instrument1 infrared0)
    (calibration_target instrument1 star2)
    (on_board instrument1 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star0)
    (mode infrared0)
    (direction star0)
    (direction star2)
    (direction planet5)
    (direction phenomenon9)
  )
  (:goal (and (pointing satellite1 planet5) (have_image phenomenon9 infrared0)))
)
