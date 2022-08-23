(define (problem roverprob6232)
  (:domain rover)
  (:objects
    camera0 - camera
    general - lander
    high_res - mode
    objective0 - objective
    rover0 - rover
    rover0store - store
    rover1 - rover
    rover1store - store
    waypoint1 - waypoint
    waypoint2 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint2 waypoint1)
    (visible waypoint1 waypoint2)
    (visible waypoint3 waypoint1)
    (at_rock_sample waypoint1)
    (at_soil_sample waypoint3)
    (at_lander general waypoint2)
    (channel_free general)
    (at rover0 waypoint3)
    (available rover0)
    (store_of rover0store rover0)
    (empty rover0store)
    (equipped_for_soil_analysis rover0)
    (can_traverse rover0 waypoint3 waypoint1)
    (at rover1 waypoint2)
    (available rover1)
    (store_of rover1store rover1)
    (empty rover1store)
    (equipped_for_rock_analysis rover1)
    (equipped_for_imaging rover1)
    (can_traverse rover1 waypoint2 waypoint1)
    (on_board camera0 rover1)
    (calibration_target camera0 objective0)
    (supports camera0 high_res)
    (visible_from objective0 waypoint2)
  )
  (:goal (and (communicated_soil_data waypoint3) (communicated_rock_data waypoint1) (communicated_image_data objective0 high_res)))
)
