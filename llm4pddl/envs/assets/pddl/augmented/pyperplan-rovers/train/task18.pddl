(define (problem roverprob3726)
  (:domain rover)
  (:objects
    camera1 - camera
    colour - mode
    general - lander
    objective0 - objective
    rover1 - rover
    rover1store - store
    waypoint0 - waypoint
    waypoint2 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint0 waypoint3)
    (visible waypoint3 waypoint0)
    (visible waypoint3 waypoint2)
    (visible waypoint2 waypoint3)
    (at_soil_sample waypoint2)
    (at_lander general waypoint0)
    (channel_free general)
    (at rover1 waypoint3)
    (available rover1)
    (store_of rover1store rover1)
    (empty rover1store)
    (equipped_for_soil_analysis rover1)
    (equipped_for_imaging rover1)
    (can_traverse rover1 waypoint3 waypoint0)
    (can_traverse rover1 waypoint0 waypoint3)
    (can_traverse rover1 waypoint3 waypoint2)
    (can_traverse rover1 waypoint2 waypoint3)
    (on_board camera1 rover1)
    (calibration_target camera1 objective0)
    (supports camera1 colour)
    (visible_from objective0 waypoint0)
  )
  (:goal (and (communicated_soil_data waypoint2) (communicated_image_data objective0 colour)))
)
