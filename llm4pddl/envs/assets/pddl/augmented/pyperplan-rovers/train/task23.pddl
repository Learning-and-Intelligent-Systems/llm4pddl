(define (problem roverprob1234)
  (:domain rover)
  (:objects
    camera0 - camera
    general - lander
    high_res - mode
    objective1 - objective
    rover0 - rover
    rover0store - store
    waypoint0 - waypoint
    waypoint3 - waypoint
  )
  (:init
    (visible waypoint3 waypoint0)
    (at_rock_sample waypoint3)
    (at_lander general waypoint0)
    (channel_free general)
    (at rover0 waypoint3)
    (available rover0)
    (store_of rover0store rover0)
    (empty rover0store)
    (equipped_for_rock_analysis rover0)
    (equipped_for_imaging rover0)
    (on_board camera0 rover0)
    (calibration_target camera0 objective1)
    (supports camera0 high_res)
    (visible_from objective1 waypoint3)
  )
  (:goal (and (communicated_rock_data waypoint3) (communicated_image_data objective1 high_res)))
)
