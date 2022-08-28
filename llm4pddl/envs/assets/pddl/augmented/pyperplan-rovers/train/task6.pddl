(define (problem roverprob4213)
  (:domain rover)
  (:objects
    camera0 - camera
    general - lander
    low_res - mode
    objective0 - objective
    objective1 - objective
    rover0 - rover
    rover0store - store
    waypoint0 - waypoint
    waypoint1 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint3 waypoint1)
    (visible waypoint0 waypoint3)
    (at_soil_sample waypoint0)
    (at_rock_sample waypoint0)
    (at_lander general waypoint1)
    (channel_free general)
    (at rover0 waypoint0)
    (available rover0)
    (store_of rover0store rover0)
    (empty rover0store)
    (equipped_for_soil_analysis rover0)
    (equipped_for_rock_analysis rover0)
    (equipped_for_imaging rover0)
    (can_traverse rover0 waypoint0 waypoint3)
    (on_board camera0 rover0)
    (calibration_target camera0 objective0)
    (supports camera0 low_res)
    (visible_from objective0 waypoint0)
    (visible_from objective1 waypoint0)
  )
  (:goal (and (communicated_soil_data waypoint0) (communicated_rock_data waypoint0) (communicated_image_data objective1 low_res)))
)
