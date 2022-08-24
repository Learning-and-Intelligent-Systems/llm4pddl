(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    infrared1 - object
    infrared3 - object
    instrument2 - object
    instrument3 - object
    instrument4 - object
    phenomenon8 - object
    planet4 - object
    planet5 - object
    satellite1 - object
    satellite2 - object
    spectrograph0 - object
    star0 - object
    star10 - object
    star2 - object
    star6 - object
    star7 - object
    star9 - object
    thermograph2 - object
  )
  (:init
    (satellite satellite1)
    (instrument instrument2)
    (supports instrument2 thermograph2)
    (calibration_target instrument2 star2)
    (instrument instrument3)
    (supports instrument3 infrared1)
    (supports instrument3 spectrograph0)
    (calibration_target instrument3 star2)
    (on_board instrument2 satellite1)
    (on_board instrument3 satellite1)
    (power_avail satellite1)
    (pointing satellite1 star6)
    (satellite satellite2)
    (instrument instrument4)
    (supports instrument4 infrared3)
    (calibration_target instrument4 star0)
    (on_board instrument4 satellite2)
    (power_avail satellite2)
    (pointing satellite2 star6)
    (mode thermograph2)
    (mode spectrograph0)
    (mode infrared1)
    (mode infrared3)
    (direction star2)
    (direction star0)
    (direction planet4)
    (direction planet5)
    (direction star6)
    (direction star7)
    (direction phenomenon8)
    (direction star9)
    (direction star10)
  )
  (:goal (and (have_image planet4 thermograph2) (have_image planet5 spectrograph0) (have_image star6 thermograph2) (have_image star7 infrared3) (have_image phenomenon8 spectrograph0) (have_image star9 infrared1) (have_image star10 infrared3)))
)
