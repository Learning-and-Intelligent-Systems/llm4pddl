(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    groundstation2 - object
    image2 - object
    instrument1 - object
    phenomenon5 - object
    planet4 - object
    satellite0 - object
  )
  (:init
    (satellite satellite0)
    (instrument instrument1)
    (supports instrument1 image2)
    (calibration_target instrument1 groundstation2)
    (on_board instrument1 satellite0)
    (power_avail satellite0)
    (pointing satellite0 planet4)
    (mode image2)
    (direction groundstation2)
    (direction planet4)
    (direction phenomenon5)
  )
  (:goal (and (have_image phenomenon5 image2)))
)