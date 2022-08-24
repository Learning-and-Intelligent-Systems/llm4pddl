(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    instrument3 - object
    phenomenon5 - object
    phenomenon7 - object
    satellite0 - object
    satellite1 - object
    spectrograph2 - object
    star0 - object
    star4 - object
  )
  (:init
    (satellite satellite0)
    (pointing satellite0 star4)
    (satellite satellite1)
    (instrument instrument3)
    (supports instrument3 spectrograph2)
    (calibration_target instrument3 star0)
    (on_board instrument3 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star0)
    (mode spectrograph2)
    (direction star0)
    (direction star4)
    (direction phenomenon5)
    (direction phenomenon7)
  )
  (:goal (and (pointing satellite0 phenomenon5) (have_image star4 spectrograph2) (have_image phenomenon5 spectrograph2) (have_image phenomenon7 spectrograph2)))
)
