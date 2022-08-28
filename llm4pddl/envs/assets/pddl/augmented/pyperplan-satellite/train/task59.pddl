(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    instrument3 - object
    phenomenon7 - object
    satellite1 - object
    spectrograph2 - object
    star0 - object
  )
  (:init
    (satellite satellite1)
    (instrument instrument3)
    (supports instrument3 spectrograph2)
    (calibration_target instrument3 star0)
    (on_board instrument3 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star0)
    (mode spectrograph2)
    (direction star0)
    (direction phenomenon7)
  )
  (:goal (and (have_image phenomenon7 spectrograph2)))
)
