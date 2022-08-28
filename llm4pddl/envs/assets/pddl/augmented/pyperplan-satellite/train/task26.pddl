(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    groundstation2 - object
    infrared0 - object
    instrument1 - object
    phenomenon6 - object
    planet4 - object
    satellite0 - object
    star7 - object
  )
  (:init
    (satellite satellite0)
    (instrument instrument1)
    (supports instrument1 infrared0)
    (calibration_target instrument1 groundstation2)
    (on_board instrument1 satellite0)
    (power_avail satellite0)
    (pointing satellite0 planet4)
    (mode infrared0)
    (direction groundstation2)
    (direction planet4)
    (direction phenomenon6)
    (direction star7)
  )
  (:goal (and (have_image phenomenon6 infrared0) (have_image star7 infrared0)))
)
