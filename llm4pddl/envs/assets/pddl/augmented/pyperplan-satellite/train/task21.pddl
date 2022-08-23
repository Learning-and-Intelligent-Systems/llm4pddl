(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    groundstation2 - object
    image2 - object
    infrared0 - object
    instrument1 - object
    phenomenon5 - object
    phenomenon6 - object
    planet3 - object
    planet4 - object
    satellite0 - object
  )
  (:init
    (satellite satellite0)
    (instrument instrument1)
    (supports instrument1 image2)
    (supports instrument1 infrared0)
    (calibration_target instrument1 groundstation2)
    (on_board instrument1 satellite0)
    (power_avail satellite0)
    (pointing satellite0 planet4)
    (mode infrared0)
    (mode image2)
    (direction groundstation2)
    (direction planet3)
    (direction planet4)
    (direction phenomenon5)
    (direction phenomenon6)
  )
  (:goal (and (have_image planet3 infrared0) (have_image planet4 infrared0) (have_image phenomenon5 image2) (have_image phenomenon6 infrared0)))
)
