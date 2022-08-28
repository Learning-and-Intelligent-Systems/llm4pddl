(define (problem strips-sat-x-1)
  (:domain satellite)
  (:objects
    groundstation2 - object
    instrument0 - object
    phenomenon6 - object
    satellite0 - object
    thermograph0 - object
  )
  (:init
    (satellite satellite0)
    (instrument instrument0)
    (supports instrument0 thermograph0)
    (calibration_target instrument0 groundstation2)
    (on_board instrument0 satellite0)
    (power_avail satellite0)
    (pointing satellite0 phenomenon6)
    (mode thermograph0)
    (direction groundstation2)
    (direction phenomenon6)
  )
  (:goal (and (have_image phenomenon6 thermograph0)))
)
