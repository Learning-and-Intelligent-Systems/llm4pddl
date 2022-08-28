(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    infrared0 - object
    instrument3 - object
    satellite1 - object
    star0 - object
    star3 - object
  )
  (:init
    (satellite satellite1)
    (instrument instrument3)
    (supports instrument3 infrared0)
    (calibration_target instrument3 star0)
    (on_board instrument3 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star0)
    (mode infrared0)
    (direction star0)
    (direction star3)
  )
  (:goal (and (have_image star3 infrared0)))
)
