(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    infrared0 - object
    instrument3 - object
    phenomenon5 - object
    satellite0 - object
    satellite1 - object
    spectrograph2 - object
    star0 - object
    star3 - object
    star4 - object
  )
  (:init
    (satellite satellite0)
    (pointing satellite0 star4)
    (satellite satellite1)
    (instrument instrument3)
    (supports instrument3 spectrograph2)
    (supports instrument3 infrared0)
    (calibration_target instrument3 star0)
    (on_board instrument3 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star0)
    (mode infrared0)
    (mode spectrograph2)
    (direction star0)
    (direction star3)
    (direction star4)
    (direction phenomenon5)
  )
  (:goal (and (pointing satellite0 phenomenon5) (have_image star3 infrared0) (have_image star4 spectrograph2)))
)
